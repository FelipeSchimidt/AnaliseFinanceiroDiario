import os
import sys
import argparse
import time
from datetime import datetime
from market_intelligence.analyzer import MarketAnalyzer
from market_intelligence.markdown_generator import MarkdownReportGenerator
from market_intelligence.pdf_generator import ExecutiveSummaryPDFGenerator
from market_intelligence.history import HistoryTracker
from market_intelligence.notifications import NotificationDispatcher


def run_daily_job(topics, recipients=None, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    history_tracker = HistoryTracker(history_dir=os.path.join(output_dir, "history"))
    dispatcher = NotificationDispatcher()

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Iniciando execução do relatório de inteligência...")

    for topic in topics:
        print(f"\n---> Processando tema: '{topic}'...")
        analyzer = MarketAnalyzer(topic)
        report = analyzer.generate_daily_report()

        # Compare with history
        comparison = history_tracker.compare_with_previous(report)
        history_tracker.save_report(report)

        # Generate Markdown
        full_md = MarkdownReportGenerator.generate_full_report(report, comparison)
        safe_topic = "".join(c if c.isalnum() else "_" for c in topic)
        md_filename = os.path.join(output_dir, f"Relatorio_{safe_topic}_{report.date}.md")
        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(full_md)
        print(f"Relatório Markdown salvo em: {md_filename}")

        # Generate PDF
        pdf_filename = os.path.join(output_dir, f"Resumo_Executivo_{safe_topic}_{report.date}.pdf")
        ExecutiveSummaryPDFGenerator.generate_pdf(report, pdf_filename)
        print(f"Resumo Executivo PDF salvo em: {pdf_filename}")

        # Dispatch Notifications
        dispatch_res = dispatcher.dispatch_all(
            topic=report.topic,
            date_str=report.date,
            summary_md=full_md[:1500] + "\n\n...[Relatório Completo em Anexo]",
            pdf_filepath=pdf_filename,
            recipients=recipients,
        )
        print("Status dos Envios:", dispatch_res)

    print("\n[✔] Processamento concluído com sucesso!")


def schedule_loop(topics, recipients, target_time="07:00"):
    print(f"Agendador ativo! Aguardando o horário das {target_time} diariamente...")
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        if current_time == target_time:
            run_daily_job(topics, recipients)
            print("Aguardando próximo dia...")
            time.sleep(60)
        time.sleep(30)


def main():
    parser = argparse.ArgumentParser(description="Análise Financeira Diária Automatizada - Inteligência de Mercado")
    parser.add_argument("--topic", type=str, action="append", help="Tópico para análise (ex: 'Bolsa Brasileira', 'Criptomoedas')")
    parser.add_argument("--email", type=str, action="append", help="Destinatários de e-mail para envio do relatório")
    parser.add_argument("--schedule", action="store_true", help="Executar modo servidor agendado diariamente às 07:00")
    parser.add_argument("--time", type=str, default="07:00", help="Horário da execução agendada (padrão: 07:00)")

    args = parser.parse_args()

    topics = args.topic if args.topic else ["Bolsa Brasileira", "Bolsa Americana", "Criptomoedas", "Commodities"]
    recipients = args.email if args.email else []

    if args.schedule:
        schedule_loop(topics, recipients, target_time=args.time)
    else:
        run_daily_job(topics, recipients)


if __name__ == "__main__":
    main()
