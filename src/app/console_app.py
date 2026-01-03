import msvcrt
from tabulate import tabulate
from src.data_manipulator import DataManager, TransactionCleaner
from src.features_builder import CustomerFeaturesBuilder, TransactionFeaturesBuilder
from src.calculations import CustomerRiskScorer, TransactionFlagger
from src.report_generator import ReportGenerator, DashboardGenerator
from src.utils import clear_screen, print_centered, show_banner, wait, error
from src.constants import *


class ConsoleApp:
    """
    This class implements a console-based application for fraud detection in banking transactions.
    It provides a menu-driven interface to load data, clean it, build features, calculate risk
    """

    def __init__(self):
        """Initialize the console application state and status flags."""
        self.current = 0
        self.df = None

        self.info = {
            'Loaded': False,
            'Cleaned': False,
            'CustomerFeatures': False,
            'TransactionFeatures': False,
            'RiskScored': False,
            'Flagged': False
        }

    def main_menu(self):
        """Display the interactive main menu and handle user keyboard navigation."""
        while True:
            clear_screen()
            show_banner()
            print("\n")

            for i, item in enumerate(MENU):
                print(SPACE, end='')
                if i == self.current:
                    print(GREEN + BOLD + item + RESET)
                else:
                    print(item)

            key = msvcrt.getch()

            if key == SPECIAL:
                key = msvcrt.getch()
                if key == UP:
                    self.current = (self.current - 1) % len(MENU)
                elif key == DOWN:
                    self.current = (self.current + 1) % len(MENU)

            elif key == ENTER:
                clear_screen()
                if self.current == 0:
                    self.load_data()
                elif self.current == 1:
                    self.clean_data()
                elif self.current == 2:
                    self.build_customer_features()
                elif self.current == 3:
                    self.build_transaction_features()
                elif self.current == 4:
                    self.calculate_risk_score()
                elif self.current == 5:
                    self.flag_transactions()
                elif self.current == 6:
                    self.show_summary()
                elif self.current == 7:
                    self.export_reports()
                elif self.current == 8:
                    self.export_dashboard()
                elif self.current == 9:
                    clear_screen()
                    print_centered("👋 Exiting FRAUDLENS ...")
                    break

    def load_data(self):
        """Load CSV files from DATA_PATH using DataManager and reset processing flags.

        After loading, all step flags are reset so only 'Loaded' is True.
        """
        show_banner()
        result = DataManager.read_csv(DATA_PATH)
        self.df = result['data_frame']
        if not len(self.df):
            print(f"{SPACE} ⚠️ We Can't Find Any Data Matched!")
            wait()
            return -1
        
        self.info = {
            'Loaded': True,
            'Cleaned': False,
            'CustomerFeatures': False,
            'TransactionFeatures': False,
            'RiskScored': False,
            'Flagged': False
        }

        table = [
            ["Rows", self.df.shape[0]],
            ["Columns", self.df.shape[1]],
            ["Matched Files", ", ".join(result['matches'])],
            ["Invalid Files", ", ".join(result['not_matches'])]
        ]

        print(f"\n{SPACE}✅ Data Loaded Successfully")
        print(tabulate(table, headers=["Metric", "Value"], tablefmt="grid"))
        wait()

    def clean_data(self):
        """Clean the loaded data using TransactionCleaner and update cleaning statistics."""
        if not self.info['Loaded']:
            error("❌ Load data first before cleaning.")
            return
        
        if self.info['Cleaned']:
            error("⚠️  Data already cleaned. Load new data to clean again.")
            return

        show_banner()
        result = TransactionCleaner.clean(self.df)
        self.df = result['cleaned_data']
        self.info['Cleaned'] = True

        stats = result['stats']
        table = [[k.replace("_", " ").title(), v] for k, v in stats.items()]

        print(f"\n{SPACE}🧹 Data Cleaning Report\n")
        print(tabulate(table, headers=["Check", "Count"], tablefmt="grid"))
        wait()

    def build_customer_features(self):
        """Construct customer-level features and mark them as built."""
        if not self.info['Loaded']:
            error("❌ Load data first.")
            return
            
        if not self.info['Cleaned']:
            error("❌ Clean data first before building customer features.")
            return
        
        if self.info['CustomerFeatures']:
            error("⚠️  Customer features already built. Load new data to rebuild.")
            return

        show_banner()
        self.df = CustomerFeaturesBuilder.build(self.df)
        self.info['CustomerFeatures'] = True

        print(f"\n{SPACE}👤 Customer Features Built Successfully")
        print(f"{SPACE}Current Shape: {self.df.shape}")
        wait()

    def build_transaction_features(self):
        """Construct transaction-level features and mark them as built."""
        if not self.info['Loaded']:
            error("❌ Load data first.")
            return
            
        if not self.info['Cleaned']:
            error("❌ Clean data first.")
            return
            
        if not self.info['CustomerFeatures']:
            error("❌ Build customer features first before building transaction features.")
            return
        
        if self.info['TransactionFeatures']:
            error("⚠️  Transaction features already built. Load new data to rebuild.")
            return

        show_banner()
        self.df = TransactionFeaturesBuilder.build(self.df)
        self.info['TransactionFeatures'] = True

        print(f"\n{SPACE}💳 Transaction Features Built Successfully")
        print(f"{SPACE}Current Shape: {self.df.shape}")
        wait()

    def calculate_risk_score(self):
        """Compute customer risk scores and update status flag."""
        if not self.info['Loaded']:
            error("❌ Load data first.")
            return
            
        if not self.info['CustomerFeatures']:
            error("❌ Build customer features first before calculating risk scores.")
            return

        show_banner()
        self.df = CustomerRiskScorer.build(self.df)
        self.info['RiskScored'] = True

        dist = self.df['risk_class'].value_counts().reset_index()
        dist.columns = ["Risk Class", "Count"]

        print(f"\n{SPACE}📊 Risk Score Distribution\n")
        print(tabulate(dist, headers="keys", tablefmt="grid"))
        wait()

    def flag_transactions(self):
        """Flag suspicious transactions using TransactionFlagger and update status flag."""
        if not self.info['Loaded']:
            error("❌ Load data first.")
            return
            
        if not self.info['TransactionFeatures']:
            error("❌ Build transaction features first before flagging transactions.")
            return

        show_banner()
        self.df = TransactionFlagger.build(self.df)
        self.info['Flagged'] = True

        flags = self.df['transaction_flag'].value_counts().reset_index()
        flags.columns = ["Flag", "Count"]

        print(f"\n{SPACE}🚨 Transaction Flag Summary\n")
        print(tabulate(flags, headers="keys", tablefmt="grid"))
        wait()

    def show_summary(self):
        """Prints summary tables: risk distribution, flag summary and top critical customers."""
        if not self.info['Loaded']:
            error("❌ Load data first.")
            return
            
        if not (self.info['RiskScored'] and self.info['Flagged']):
            error("❌ Run risk scoring and transaction flagging first.")
            return

        show_banner()

        risk_dist = self.df['risk_class'].value_counts().reset_index()
        risk_dist.columns = ["Risk Class", "Count"]

        total_tx = len(self.df)
        flagged_tx = self.df['transaction_flag'].sum()

        flag_table = [
            ["Total Transactions", total_tx],
            ["Flagged Transactions", flagged_tx],
            ["Flag Rate (%)", f"{(flagged_tx / total_tx) * 100:.2f}%"]
        ]

        top_risk = (
            self.df[self.df['risk_class'] == 'critical']
            [['nameOrig', 'risk_score']]
            .drop_duplicates('nameOrig')
            .sort_values('risk_score', ascending=False)
            .head(5)
        )

        print(f"\n{SPACE}📊 Risk Distribution\n")
        print(tabulate(risk_dist, headers="keys", tablefmt="grid"))

        print(f"\n{SPACE}🚨 Flag Summary\n")
        print(tabulate(flag_table, headers=["Metric", "Value"], tablefmt="grid"))

        print(f"\n{SPACE}🔥 Top 5 Critical Customers\n")
        if top_risk.empty:
            print(f"{SPACE}- No critical customers found.")
        else:
            print(tabulate(top_risk, headers="keys", tablefmt="grid"))

        wait()

    def export_reports(self):
        """Generate CSV and text reports and display their output paths."""
        if not self.info['Loaded']:
            error("❌ Load data first.")
            return
            
        if not (self.info['RiskScored'] and self.info['Flagged']):
            error("❌ Run risk scoring and transaction flagging first.")
            return

        show_banner()
        gen = ReportGenerator(self.df)
        paths = gen.export_all()

        table = [[k.replace("_", " ").title(), v] for k, v in paths.items()]

        print(f"\n{SPACE}📁 Reports Exported Successfully\n")
        print(tabulate(table, headers=["Report", "Path"], tablefmt="grid"))
        wait()

    def export_dashboard(self):
        """Generate a PDF dashboard and display its path."""
        if not self.info['Loaded']:
            error("❌ Load data first.")
            return
            
        if not (self.info['RiskScored'] and self.info['Flagged']):
            error("❌ Run risk scoring and transaction flagging first.")
            return

        show_banner()
        dashboard = DashboardGenerator(self.df)
        path = dashboard.export_dashboard_pdf()

        print(f"\n{SPACE}📊 Dashboard Exported Successfully\n")
        print(f"{SPACE}Path: {path}")
        wait()