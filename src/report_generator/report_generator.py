import os
import pandas as pd
from datetime import datetime


class ReportGenerator:
    """
    Generate comprehensive CSV and TXT reports with detailed analytics.
    """

    def __init__(self, df: pd.DataFrame, output_dir: str = "outputs"):
        """Initialize the report generator with a DataFrame and output directory."""
        self.df = df.copy()
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export_flagged_transactions(self) -> str:
        """Export detailed flagged transactions with additional context"""
        path = os.path.join(self.output_dir, "flagged_transactions.csv")
        
        flagged = self.df[self.df['transaction_flag'] == 1].copy()
        
        customer_totals = self.df.groupby('nameOrig')['amount'].sum()
        flagged['customer_total_volume'] = flagged['nameOrig'].map(customer_totals)
        flagged['pct_of_customer_volume'] = (
            flagged['amount'] / flagged['customer_total_volume'] * 100
        ).round(2)
        
        cols = ['nameOrig', 'nameDest', 'amount', 'type', 'risk_score', 
                'risk_class', 'transaction_flag', 'oldbalanceOrg', 
                'newbalanceOrig', 'pct_of_customer_volume']
        
        available_cols = [col for col in cols if col in flagged.columns]
        flagged[available_cols].to_csv(path, index=False)
        
        return path

    def export_customer_risk_summary(self) -> str:
        """Export comprehensive customer risk analysis"""
        path = os.path.join(self.output_dir, "customer_risk_summary.csv")

        customer_stats = self.df.groupby('nameOrig').agg({
            'amount': ['sum', 'mean', 'count', 'max'],
            'transaction_flag': 'sum',
            'risk_score': 'first',
            'risk_class': 'first'
        }).reset_index()
        
        customer_stats.columns = [
            'customer_id', 'total_amount', 'avg_amount', 'transaction_count',
            'max_transaction', 'flagged_count', 'risk_score', 'risk_class'
        ]
        
        customer_stats['flagged_percentage'] = (
            customer_stats['flagged_count'] / customer_stats['transaction_count'] * 100
        ).round(2)
        
        customer_stats['risk_rank'] = customer_stats['risk_score'].rank(
            ascending=False, method='min'
        ).astype(int)
        
        customer_stats = customer_stats.sort_values('risk_score', ascending=False)
        
        customer_stats.to_csv(path, index=False)
        return path

    def export_text_report(self) -> str:
        """Generate comprehensive text report with detailed insights"""
        path = os.path.join(self.output_dir, "report.txt")

        total_transactions = len(self.df)
        total_customers = self.df['nameOrig'].nunique()
        total_recipients = self.df['nameDest'].nunique()
        flagged_count = int(self.df['transaction_flag'].sum())
        flagged_rate = (flagged_count / total_transactions * 100)
        
        total_amount = self.df['amount'].sum()
        avg_amount = self.df['amount'].mean()
        median_amount = self.df['amount'].median()
        max_amount = self.df['amount'].max()
        
        avg_risk_score = self.df['risk_score'].mean()
        
        risk_dist = self.df['risk_class'].value_counts()
        
        top_customers = (
            self.df[['nameOrig', 'risk_score', 'risk_class']]
            .drop_duplicates('nameOrig')
            .sort_values('risk_score', ascending=False)
            .head(15)
        )
        
        type_stats = self.df.groupby('type').agg({
            'amount': 'count',
            'transaction_flag': 'sum'
        })
        
        flagged_customers = self.df[self.df['transaction_flag'] == 1].groupby('nameOrig').size()
        top_flagged = flagged_customers.sort_values(ascending=False).head(10)
        
        high_value_flagged = (
            self.df[self.df['transaction_flag'] == 1]
            .nlargest(10, 'amount')[['nameOrig', 'nameDest', 'amount', 'type', 'risk_score']]
        )

        with open(path, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write("FRAUDLENS – COMPREHENSIVE FRAUD DETECTION ANALYSIS REPORT\n")
            f.write("=" * 70 + "\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Prepared by: Ahmed Sharaf - ITI AI Track\n")
            f.write("=" * 70 + "\n\n")

            f.write("EXECUTIVE SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Transactions Analyzed:      {total_transactions:,}\n")
            f.write(f"Unique Customers:                 {total_customers:,}\n")
            f.write(f"Unique Recipients:                {total_recipients:,}\n")
            f.write(f"Flagged Transactions:             {flagged_count:,} ({flagged_rate:.2f}%)\n")
            f.write(f"Average Risk Score:               {avg_risk_score:.2f}\n")
            f.write(f"Total Transaction Volume:         ${total_amount:,.2f}\n")
            f.write(f"Average Transaction Amount:       ${avg_amount:,.2f}\n")
            f.write(f"Median Transaction Amount:        ${median_amount:,.2f}\n")
            f.write(f"Maximum Transaction Amount:       ${max_amount:,.2f}\n")
            f.write("\n")

            f.write("RISK CLASS DISTRIBUTION\n")
            f.write("-" * 70 + "\n")
            for risk_class, count in risk_dist.items():
                percentage = (count / total_transactions * 100)
                f.write(f"{risk_class:15} : {count:6,} customers ({percentage:5.2f}%)\n")
            f.write("\n")

            f.write("TRANSACTION TYPE ANALYSIS\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'Type':<15} {'Count':<12} {'Flagged':<12} {'Flag Rate':<12}\n")
            f.write("-" * 70 + "\n")
            for tx_type in type_stats.index:
                count = type_stats.loc[tx_type, 'amount']
                flagged = type_stats.loc[tx_type, 'transaction_flag']
                rate = (flagged / count * 100) if count > 0 else 0
                f.write(f"{tx_type:<15} {count:<12,} {int(flagged):<12,} {rate:<12.2f}%\n")
            f.write("\n")

            f.write("TOP 15 HIGH-RISK CUSTOMERS\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'Rank':<6} {'Customer ID':<20} {'Risk Score':<12} {'Risk Class':<15}\n")
            f.write("-" * 70 + "\n")
            for idx, row in enumerate(top_customers.itertuples(index=False), 1):
                f.write(
                    f"{idx:<6} {row.nameOrig:<20} {row.risk_score:<12.2f} {row.risk_class:<15}\n"
                )
            f.write("\n")

            f.write("TOP 10 CUSTOMERS BY FLAGGED TRANSACTION COUNT\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'Rank':<6} {'Customer ID':<30} {'Flagged Count':<15}\n")
            f.write("-" * 70 + "\n")
            for idx, (customer, count) in enumerate(top_flagged.items(), 1):
                f.write(f"{idx:<6} {customer:<30} {count:<15}\n")
            f.write("\n")

            f.write("TOP 10 HIGH-VALUE FLAGGED TRANSACTIONS\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'From':<15} {'To':<15} {'Amount':<15} {'Type':<12} {'Risk':<10}\n")
            f.write("-" * 70 + "\n")
            for _, row in high_value_flagged.iterrows():
                f.write(
                    f"{row['nameOrig'][:14]:<15} "
                    f"{row['nameDest'][:14]:<15} "
                    f"${row['amount']:>13,.2f} "
                    f"{row['type']:<12} "
                    f"{row['risk_score']:<10.2f}\n"
                )
            f.write("\n")

            f.write("KEY FINDINGS & RECOMMENDATIONS\n")
            f.write("-" * 70 + "\n")
            
            if flagged_rate > 10:
                f.write(f"• HIGH ALERT: {flagged_rate:.1f}% transaction flag rate detected.\n")
                f.write("  Recommendation: Immediate review of flagged transactions required.\n\n")
            elif flagged_rate > 5:
                f.write(f"• MODERATE CONCERN: {flagged_rate:.1f}% transaction flag rate.\n")
                f.write("  Recommendation: Enhanced monitoring recommended.\n\n")
            else:
                f.write(f"• LOW RISK: {flagged_rate:.1f}% transaction flag rate.\n")
                f.write("  Recommendation: Continue standard monitoring protocols.\n\n")
            
            high_risk_count = (self.df['risk_class'].isin(['High', 'Critical'])).sum()
            high_risk_pct = (high_risk_count / len(self.df) * 100)
            f.write(f"• {high_risk_count:,} transactions ({high_risk_pct:.1f}%) from High/Critical risk customers.\n")
            f.write("  Recommendation: Implement enhanced due diligence for these accounts.\n\n")
            
            if 'TRANSFER' in type_stats.index:
                transfer_flag_rate = (
                    type_stats.loc['TRANSFER', 'transaction_flag'] / 
                    type_stats.loc['TRANSFER', 'amount'] * 100
                )
                if transfer_flag_rate > 5:
                    f.write(f"• TRANSFER transactions show {transfer_flag_rate:.1f}% flag rate.\n")
                    f.write("  Recommendation: Review transfer transaction limits and monitoring rules.\n\n")
            
            top_10_customers = self.df.groupby('nameOrig')['amount'].sum().nlargest(10).sum()
            concentration = (top_10_customers / total_amount * 100)
            f.write(f"• Top 10 customers represent {concentration:.1f}% of total transaction volume.\n")
            if concentration > 30:
                f.write("  Recommendation: Monitor concentration risk and diversify customer base.\n\n")
            else:
                f.write("  Recommendation: Customer base shows healthy diversification.\n\n")

            f.write("=" * 70 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 70 + "\n")
            f.write("\nFor questions or additional analysis, contact: Ahmed Sharaf\n")
            f.write("FraudLens - AI-Driven Fraud Detection System\n")

        return path

    def export_all(self) -> dict:
        """Export all reports and return file paths"""
        return {
            "flagged_csv": self.export_flagged_transactions(),
            "customer_risk_csv": self.export_customer_risk_summary(),
            "text_report": self.export_text_report()
        }