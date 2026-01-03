import os
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER


class DashboardGenerator:
    """
    Generate a statistical analysis PDF dashboard focusing on critical customers.
    """

    def __init__(self, df, output_dir: str = "outputs"):
        """Create a DashboardGenerator for the given DataFrame and ensure output folders exist."""
        self.df = df.copy()
        self.output_dir = output_dir
        self.output_chart_dir = os.path.join(output_dir, 'charts')
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.output_chart_dir, exist_ok=True)
        plt.style.use('seaborn-v0_8-whitegrid')
        

    def _create_beautiful_logo(self):
        """Create a beautiful gradient-style logo"""
        fig, ax = plt.subplots(figsize=(4, 4), facecolor='none')
        
        circle1 = plt.Circle((0.5, 0.5), 0.45, color='#1a237e', alpha=0.8)
        circle2 = plt.Circle((0.5, 0.5), 0.35, color='#283593', alpha=0.9)
        circle3 = plt.Circle((0.5, 0.5), 0.25, color='#3949ab', alpha=1.0)
        
        ax.add_patch(circle1)
        ax.add_patch(circle2)
        ax.add_patch(circle3)
        
        ax.text(0.5, 0.5, 'FL', fontsize=70, weight='bold', ha='center', va='center', color='white', family='sans-serif')
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        path = os.path.join(self.output_chart_dir, "logo.png")
        plt.savefig(path, bbox_inches='tight', transparent=True, dpi=200)
        plt.close()
        return path

    def _save_critical_customers_by_risk_class(self):
        """Histogram showing number of critical customers by risk class"""
        counts = self.df['risk_class'].value_counts().sort_index()
        risk_order = ['low', 'medium', 'high', 'critical']        
        ordered_counts = {}
        for risk in risk_order:
            if risk in counts.index:
                ordered_counts[risk] = counts[risk]
        
        for risk in risk_order:
            if risk not in ordered_counts:
                ordered_counts[risk] = 0
        
        labels = list(ordered_counts.keys())
        values = list(ordered_counts.values())
        
        critical_count = ordered_counts.get('critical', 0)
        
        colors_list = []
        for label in labels:
            if label == 'critical':
                colors_list.append('#F44336')
            else:
                colors_list.append('#E0E0E0')
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(range(len(labels)), values, 
                      color=colors_list,
                      edgecolor='black', linewidth=1.5, alpha=0.85)
        
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels([l.capitalize() for l in labels], fontsize=13, weight='bold')
        ax.set_xlabel('Risk Class', fontsize=14, weight='bold', color='#1a237e')
        ax.set_ylabel('Number of Customers', fontsize=14, weight='bold', color='#1a237e')
        ax.set_title(f'Critical Customers: {critical_count:,}', 
                     fontsize=18, weight='bold', pad=20, color='#F44336')
        
        for i, bar in enumerate(bars):
            height = bar.get_height()
            label_text = f'{int(height):,}'
            if labels[i] == 'critical':
                label_text = f'{int(height):,}\n(CRITICAL)'
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        label_text,
                        ha='center', va='bottom', fontsize=12, weight='bold',
                        color='#F44336')
            else:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        label_text,
                        ha='center', va='bottom', fontsize=11, weight='bold')
        
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_axisbelow(True)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        plt.tight_layout()
        
        path = os.path.join(self.output_chart_dir, "critical_by_risk_class.png")
        plt.savefig(path, bbox_inches='tight', dpi=150, facecolor='white')
        plt.close()
        return path

    def _save_critical_customers_by_transaction_flag(self):
        """Histogram showing critical customers by transaction flag status"""
        critical_df = self.df[self.df['risk_class'] == 'critical']
                
        flag_counts = critical_df['transaction_flag'].value_counts()
        
        labels = ['Normal', 'Flagged']
        values = [
            flag_counts.get(0, 0),
            flag_counts.get(1, 0)
        ]
                
        colors_list = ['#FF9800', '#F44336']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(range(len(labels)), values, 
                      color=colors_list,
                      edgecolor='black', linewidth=1.5, alpha=0.85)
        
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=13, weight='bold')
        ax.set_xlabel('Transaction Status', fontsize=14, weight='bold', color='#1a237e')
        ax.set_ylabel('Number of Critical Customers', fontsize=14, weight='bold', color='#1a237e')
        ax.set_title(f'Critical Customers by Transaction Flag (Total: {sum(values):,})', 
                     fontsize=18, weight='bold', pad=20, color='#F44336')
        
        total = sum(values)
        for bar in bars:
            height = bar.get_height()
            percentage = (height / total * 100) if total > 0 else 0
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}\n({percentage:.1f}%)',
                    ha='center', va='bottom', fontsize=11, weight='bold')
        
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_axisbelow(True)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        plt.tight_layout()
        
        path = os.path.join(self.output_chart_dir, "critical_by_flag.png")
        plt.savefig(path, bbox_inches='tight', dpi=150, facecolor='white')
        plt.close()
        return path

    def _save_critical_customers_by_payment_type(self):
        """Histogram showing critical customers by payment type"""
        critical_df = self.df[self.df['risk_class'] == 'critical']
        
        type_counts = critical_df['type'].value_counts().sort_values(ascending=False)
                
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors_bar = ['#D32F2F', '#E53935', '#F44336', '#EF5350', '#E57373']
        bars = ax.bar(range(len(type_counts)), type_counts.values, 
                      color=colors_bar[:len(type_counts)],
                      edgecolor='black', linewidth=1.5, alpha=0.85)
        
        ax.set_xticks(range(len(type_counts)))
        ax.set_xticklabels(type_counts.index, fontsize=13, weight='bold', rotation=0)
        ax.set_xlabel('Payment Type', fontsize=14, weight='bold', color='#1a237e')
        ax.set_ylabel('Number of Critical Customers', fontsize=14, weight='bold', color='#1a237e')
        ax.set_title(f'Critical Customers by Payment Type (Total: {type_counts.sum():,})', 
                     fontsize=18, weight='bold', pad=20, color='#F44336')
        
        total = type_counts.sum()
        for bar in bars:
            height = bar.get_height()
            percentage = (height / total * 100) if total > 0 else 0
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}\n({percentage:.1f}%)',
                    ha='center', va='bottom', fontsize=11, weight='bold')
        
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.set_axisbelow(True)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))
        
        plt.tight_layout()
        
        path = os.path.join(self.output_chart_dir, "critical_by_payment_type.png")
        plt.savefig(path, bbox_inches='tight', dpi=150, facecolor='white')
        plt.close()
        return path

    def export_dashboard_pdf(self) -> str:
        """Generate critical customer analysis dashboard"""
        pdf_path = os.path.join(self.output_dir, "Dashboard.pdf")
        styles = getSampleStyleSheet()
        
        main_title_style = ParagraphStyle(
            'MainTitle',
            parent=styles['Title'],
            fontSize=42,
            textColor=colors.HexColor('#1a237e'),
            alignment=TA_CENTER,
            spaceAfter=15,
            fontName='Helvetica-Bold',
            leading=50
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontSize=20,
            textColor=colors.HexColor('#283593'),
            alignment=TA_CENTER,
            spaceAfter=8,
            fontName='Helvetica',
            leading=24
        )
        
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#5e35b1'),
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica'
        )
        
        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=colors.HexColor('#F44336'),
            spaceAfter=25,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        pdf = SimpleDocTemplate(pdf_path, pagesize=A4,
                                topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []

        logo_path = self._create_beautiful_logo()
        
        elements.append(Spacer(1, 60))
        elements.append(Image(logo_path, width=3*inch, height=3*inch))
        elements.append(Spacer(1, 25))
        
        elements.append(Paragraph("FRAUDLENS", main_title_style))
        elements.append(Paragraph(
            "Critical Customer Analysis Dashboard",
            subtitle_style
        ))
        elements.append(Paragraph(
            "High-Risk Customer Detection & Monitoring",
            info_style
        ))
        
        elements.append(Spacer(1, 80))
        
        line_table = Table([['_' * 80]], colWidths=[6*inch])
        line_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#5e35b1')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 14)
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 40))
        
        author_style = ParagraphStyle(
            'Author',
            parent=styles['Normal'],
            fontSize=16,
            textColor=colors.HexColor('#1a237e'),
            alignment=TA_CENTER,
            spaceAfter=8,
            fontName='Helvetica-Bold'
        )
        
        affiliation_style = ParagraphStyle(
            'Affiliation',
            parent=styles['Normal'],
            fontSize=13,
            textColor=colors.HexColor('#5e35b1'),
            alignment=TA_CENTER,
            spaceAfter=4,
            fontName='Helvetica'
        )
        
        elements.append(Paragraph("Created By", info_style))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("Ahmed Sharaf", author_style))
        elements.append(Paragraph(
            "Information Technology Institute (ITI)",
            affiliation_style
        ))
        elements.append(Paragraph(
            "Artificial Intelligence Professional Track",
            affiliation_style
        ))
        
        elements.append(Spacer(1, 50))
        
        from datetime import datetime
        date_style = ParagraphStyle(
            'Date',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#757575'),
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        elements.append(Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            date_style
        ))
        
        elements.append(PageBreak())

        elements.append(Paragraph("Critical Customer Analysis", heading_style))
        elements.append(Spacer(1, 15))
        
        risk_hist = self._save_critical_customers_by_risk_class()
        flag_hist = self._save_critical_customers_by_transaction_flag()
        payment_hist = self._save_critical_customers_by_payment_type()
        
        elements.append(Image(risk_hist, width=6.5*inch, height=4.5*inch))
        elements.append(Spacer(1, 20))
        
        elements.append(Image(flag_hist, width=6.5*inch, height=4.5*inch))
        
        elements.append(PageBreak())

        elements.append(Paragraph("Critical Customers by Payment Type", heading_style))
        elements.append(Spacer(1, 20))
        
        elements.append(Image(payment_hist, width=7*inch, height=4.5*inch))
        elements.append(Spacer(1, 30))
        
        summary_subtitle = ParagraphStyle(
            'SummarySubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=15,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        elements.append(Paragraph("Critical Customer Statistics", summary_subtitle))
        
        critical_df = self.df[self.df['risk_class'] == 'critical']
        total_transactions = len(self.df)
        critical_count = len(critical_df)
        critical_pct = (critical_count / total_transactions * 100) if total_transactions > 0 else 0
        critical_unique = critical_df['nameOrig'].nunique() if 'nameOrig' in critical_df.columns else 0
        critical_flagged = critical_df['transaction_flag'].sum() if 'transaction_flag' in critical_df.columns else 0
        critical_flagged_pct = (critical_flagged / critical_count * 100) if critical_count > 0 else 0
        avg_risk_critical = critical_df['risk_score'].mean() if len(critical_df) > 0 and 'risk_score' in critical_df.columns else 0
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Critical Customers', f"{critical_count:,}"],
            ['% of Total Transactions', f"{critical_pct:.2f}%"],
            ['Unique Critical Customers', f"{critical_unique:,}"],
            ['Flagged Critical Transactions', f"{int(critical_flagged):,} ({critical_flagged_pct:.2f}%)"],
            ['Avg Risk Score (Critical)', f"{avg_risk_critical:.2f}"],
            ['Payment Types (Critical)', f"{critical_df['type'].nunique() if len(critical_df) > 0 else 0}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F44336')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 13),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
            ('TOPPADDING', (0, 0), (-1, 0), 15),
            ('GRID', (0, 0), (-1, -1), 1.5, colors.HexColor('#F44336')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
             [colors.HexColor('#ffebee'), colors.white]),
            ('TOPPADDING', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 12)
        ]))
        
        elements.append(summary_table)

        pdf.build(elements)
        return pdf_path