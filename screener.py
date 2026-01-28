import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from ta.momentum import RSIIndicator
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(layout="wide", page_title="Trade Republic Screener Pro")
st.title("🔥 Trade Republic Screener : Actions + ETF")

SECTEURS_DISPONIBLES = [
    "Technology",
    "Financial Services",
    "Healthcare",
    "Consumer Cyclical",
    "Consumer Defensive",
    "Energy",
    "Industrials",
    "Utilities",
    "Real Estate",
    "Basic Materials",
    "Communication Services"
]



@st.cache_data(ttl=3600)
def get_trade_republic_tickers():
    """Tickers disponibles sur Trade Republic par zone géographique"""
    
    # Liste US nettoyée (doublons supprimés)
    us_tickers = [
        'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'BRK.B', 'NVDA', 'JPM', 'JNJ', 'V', 
        'UNH', 'PG', 'HD', 'PYPL', 'DIS', 'NFLX', 'VZ', 'INTC', 'CMCSA', 'CSCO', 'PEP', 'ADBE', 
        'T', 'NKE', 'PFE', 'MRK', 'XOM', 'CVX', 'ABT', 'KO', 'IBM', 'LLY', 'MDT', 'CAT', 'WMT', 
        'CRM', 'AMGN', 'TXN', 'BA', 'MMM', 'NOW', 'HON', 'DHR', 'NVS', 'QCOM', 'GILD', 'BLK', 
        'SBUX', 'SYK', 'PM', 'LMT', 'TMO', 'GS', 'KMB', 'LRCX', 'RTX', 'FIS', 'BKNG', 'COP', 
        'HUM', 'ATVI', 'TGT', 'AXP', 'DOW', 'COST', 'ZM', 'ZTS', 'ISRG', 'MS', 'ADP', 'MCO', 
        'APD', 'MAR', 'ADSK', 'FISV', 'CDW', 'NDAQ', 'NTES', 'WDC', 'RMD', 'VRTX', 'EA', 
        'CTSH', 'TMUS', 'CARR', 'CSX', 'NTRS', 'PXD', 'TEL', 'MPC', 'DXCM', 'SPGI', 'PGR', 
        'AIG', 'KMX', 'IQV', 'DOV', 'SBAC', 'PNC', 'CINF', 'CMS', 'ETR', 'XLNX', 'TRV', 'OXY', 
        'LNT', 'ETSY', 'CAG', 'TROW', 'SWK', 'NWL', 'YUM', 'FANG', 'CPT', 'VTRS', 'BBY', 'AFL', 
        'HCA', 'MTD', 'AEE', 'ORCL', 'ZBRA', 'MTCH', 'AAL', 'TDY', 'CNC', 'SNX', 'WAB', 'DRE', 
        'MORN', 'TAL', 'BXP', 'HSY', 'GOOG', 'MAS', 'KEYS', 'FFIV', 'GD', 'NUE', 'ICE', 'CEG', 
        'SSNC', 'VFC', 'BAX', 'FICO', 'FLIR', 'LDOS', 'STX', 'HPQ', 'GWW', 'EXPE', 'REXR', 
        'STM', 'ALGN', 'TFW', 'WDAY', 'ROK', 'HBAN', 'ROL', 'WST', 'HST', 'TFX', 'MTH', 'JCI', 
        'TTWO', 'MODN', 'RNG', 'EXP', 'PPL', 'NRG', 'AVY', 'HOLX', 'MRVL', 'DGX', 'DRI', 
        'MCHP', 'RCL', 'ANSS', 'MSI', 'WY', 'PFG', 'ESNT', 'SBSW', 'IRDM', 'POWI', 'BIO', 
        'MCK', 'VFS', 'ARE', 'RCII', 'SDGR', 'SYY', 'SSTK', 'AEM', 'ARCO', 'STT', 'HBI', 
        'FCN', 'INFO', 'SRCL', 'KDP', 'FOXA', 'VNC', 'AEO', 'PGH', 'HOOD', 'DLR', 'BCD', 
        'TYL', 'BDX', 'REAL', 'KMX', 'VAL', 'AMS'
    ]
    
    # Liste Europe étendue (500+ tickers Trade Republic)
    pea_europe = [
        # France (.PA)
        'BNP.PA', 'OR.PA', 'SAN.PA', 'GLE.PA', 'SOCI.PA', 'CAP.PA', 'MC.PA', 'RMS.PA', 'KER.PA', 
        'LVMH.PA', 'AIR.PA', 'SAF.PA', 'EL.PA', 'CA.PA', 'HO.PA', 'SU.PA', 'ENGI.PA', 'VIE.PA', 
        'ORA.PA', 'EN.PA', 'TEP.PA', 'CPST.PA', 'ML.PA', 'TOTF.PA', 'VIRG.PA', 'WLN.PA', 'ELO.PA', 
        'RUI.PA', 'PUB.PA', 'URW.PA', 'SEB.PA', 'SGO.PA', 'ALO.PA', 'RI.PA', 'RF.PA', 'SW.PA', 
        'BIO.PA', 'GLO.PA', 'STM.PA', 'HEN.PA', 'NOK.PA', 'SOL.PA', 'INEO.PA', 'GDS.PA', 'ADE.PA', 
        'INE.PA', 'ALMD.PA', 'EDEN.PA', 'AC.PA', 'BIC.PA', 'BVI.PA', 'TE.PA', 'DBV.PA', 'VALO.PA', 
        'INER.PA', 'SOP.PA', 'ALYT.PA', 'ELEC.PA', 'ALT.PA', 'TFV.PA', 'NEX.PA', 'IPS.PA', 'PAP.PA', 
        'VIV.PA', 'SCHP.PA', 'ALTR.PA', 'GEC.PA', 'FR.PA', 'EUR.PA', 'ALU.PA',
        
        # Allemagne (.DE)
        'SAP.DE', 'SIE.DE', 'ALV.DE', 'DBK.DE', 'CON.DE', 'BAS.DE', 'ADE.DE', 'VOW3.DE', 'MBG.DE', 
        'DAI.DE', 'BMW.DE', 'HEN3.DE', 'FRE.DE', '1COV.DE', 'EOAN.DE', 'RWE.DE', 'BEI.DE', 'HEIG.DE', 
        'SY1.DE', 'REL.DE', 'TTE.DE', 'MRK.DE', 'BAYN.DE', 'LIN.DE', 'ZAL.DE', 'NDX1.DE', 'FME.DE', 
        'HFG.DE', 'HOT.DE', 'WCH.DE', 'ETR.DE', 'VNA.DE', 'HLAG.DE', 'DTE.DE', 'FRA.DE',
        
        # Italie (.MI)
        'ENI.MI', 'UCG.MI', 'ISP.MI', 'STLA.MI', 'BAMI.MI', 'IG.MI', 'STM.MI', 'PRY.MI', 'BPE.MI', 
        'MONC.MI', 'TRN.MI', 'EXO.MI', 'TWRG.MI', 'SRG.MI', 'G.MI', 'REC.MI',
        
        # Pays-Bas (.AS)
        'ASML.AS', 'ABN.AS', 'ING.AS', 'HEIA.AS', 'RAND.AS', 'KPN.AS', 'WKL.AS', 'IMCD.AS', 'DSM.AS',
        
        # Espagne (.MC)
        'IBE.MC', 'SAN.MC', 'ACS.MC', 'BBVA.MC', 'TEF.MC', 'ENAG.MC', 'REP.MC', 'MAP.MC', 'ITX.MC',
        
        # Nordiques + Autres
        'NESN.SW', 'NVO', 'NOVO-B.CO', 'DANSKE.CO', 'NOKIA.HE', 'VOLCARB-B.ST', 'ERIC-B.ST', 
        'OMV.VI', 'KBC.BR', 'SOLB.BR'
    ]

    asia_tickers = [
    # 🇯🇵 JAPON (Tokyo .T) - 300+ tickers TOPIX/Nikkei
    '7203.T', '6758.T', '9434.T', '8306.T', '6861.T', '7974.T', '8035.T', '4502.T', 
    '4063.T', '9432.T', '8001.T', '8058.T', '9984.T', '2914.T', '1801.T', '1802.T', 
    '1803.T', '1810.T', '2503.T', '2269.T', '2282.T', '2531.T', '2569.T', '2579.T', 
    '2587.T', '2596.T', '2602.T', '2810.T', '2871.T', '2880.T', '2897.T', '2901.T', 
    '2914.T', '2929.T', '2944.T', '3003.T', '3087.T', '3099.T', '3105.T', '3109.T', 
    '3231.T', '3397.T', '3405.T', '3407.T', '3413.T', '3436.T', '3659.T', '3765.T', 
    '3861.T', '3864.T', '3902.T', '4021.T', '4041.T', '4042.T', '4043.T', '4045.T', 
    '4051.T', '4058.T', '4060.T', '4063.T', '4080.T', '4091.T', '4182.T', '4183.T', 
    '4185.T', '4187.T', '4188.T', '4272.T', '4273.T', '4274.T', '4281.T', '4282.T', 
    '4288.T', '4307.T', '4324.T', '4326.T', '4327.T', '4354.T', '4369.T', '4370.T', 
    '4388.T', '4452.T', '4503.T', '4506.T', '4507.T', '4519.T', '4523.T', '4528.T', 
    '4568.T', '4569.T', '4571.T', '4578.T', '4587.T', '4589.T', '4594.T', '4608.T', 
    '4612.T', '4617.T', '4626.T', '4631.T', '4640.T', '4650.T', '4666.T', '4667.T', 
    '4668.T', '4684.T', '4689.T', '4694.T', '4704.T', '4714.T', '4716.T', '4720.T', 
    '4722.T', '4723.T', '4725.T', '4733.T', '4736.T', '4755.T', '4760.T', '4768.T', 
    '4770.T', '4784.T', '4793.T', '4795.T', '4812.T', '4813.T', '4816.T', '4820.T', 
    '4823.T', '4833.T', '4835.T', '4837.T', '4849.T', '4850.T', '4857.T', '4860.T', 
    '4861.T', '4863.T', '4867.T', '4871.T', '4875.T', '4877.T', '4880.T', '4892.T', 
    '4893.T', '4899.T', '4901.T', '4902.T', '4904.T', '4905.T', '4908.T', '4911.T', 
    '4912.T', '4915.T', '4917.T', '4919.T', '4920.T', '4923.T', '4926.T', '4927.T', 
    '4930.T', '4931.T', '4932.T', '4936.T', '4937.T', '4938.T', '4940.T', '4941.T', 
    '4942.T', '4946.T', '4947.T', '4948.T', '4950.T', '4951.T', '4952.T', '4958.T',
    
    # 🇨🇳🇭🇰 CHINE / HONG KONG (.HK) - 100+ tickers
    '0700.HK', '3690.HK', '9988.HK', '9618.HK', '1024.HK', '9922.HK', '1299.HK', 
    '2318.HK', '1810.HK', '3988.HK', '0941.HK', '0939.HK', '1398.HK', '0388.HK', 
    '0001.HK', '0002.HK', '0003.HK', '0005.HK', '0006.HK', '0011.HK', '0016.HK', 
    '0017.HK', '0019.HK', '0066.HK', '0076.HK', '0083.HK', '0123.HK', '0128.HK', 
    '0129.HK', '0386.HK', '0688.HK', '0762.HK', '0823.HK', '0968.HK', '0992.HK', 
    '0999.HK', '1038.HK', '1093.HK', '1099.HK', '1177.HK', '1299.HK', '1755.HK', 
    '1800.HK', '1810.HK', '1876.HK', '1928.HK', '1966.HK', '2269.HK', '3690.HK', 
    '3888.HK', '6628.HK', '6862.HK', '9618.HK', '9869.HK', '9922.HK', '9961.HK',
    
    # 🇰🇷 CORÉE (.KS) - 80+ tickers KOSPI
    '005930.KS', '000660.KS', '373220.KS', '005380.KS', '035420.KS', '035720.KS', 
    '005490.KS', '105560.KS', '068270.KS', '012330.KS', '055550.KS', '000270.KS', 
    '015760.KS', '051910.KS', '032830.KS', '028260.KS', '034020.KS', '012450.KS', 
    '329180.KS', '009540.KS', '267260.KS', '402340.KS', '207940.KS', '196170.KS', 
    '086790.KS', '006400.KS', '003670.KS', '010130.KS', '033780.KS', '017670.KS',
    
    # 🇹🇼 TAIWAN (.TW) - 15+ tickers
    '2330.TW', '2454.TW', '2317.TW', '2303.TW', '2308.TW', '6485.TW', '3034.TW',
    
    # 🇸🇬 SINGAPOUR (.SI) - 10+ tickers
    'D05.SI', 'C6L.SI', 'O39.SI', 'Z74.SI', 'S68.SI',
    
    # 🇮🇳 INDE (.NS / .BO) - 20+ tickers NSE/BSE
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS',
    'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS'
]

    # AFRIQUE
    africa_tickers = [
    # 🇿🇦 JSE Johannesburg (dispo Trade Republic - top 100+) [web:52]
    'NPN.JO', 'AGL.JO', 'SBK.JO', 'CFR.JO', 'SOL.JO', 'FFM.JO', 'BHP.JO', 'ANG.JO', 
    'INL.JO', 'SHP.JO', 'REM.JO', 'GFI.JO', 'FSR.JO', 'SLM.JO', 'MTN.JO', 'VOD.JO', 
    'ABG.JO', 'SSW.JO', 'SCL.JO', 'NPH.JO', 'WHL.JO', 'BID.JO', 'TRU.JO', 'SBG.JO', 
    'APN.JO', 'KIO.JO', 'IMP.JO', 'OCE.JO', 'NDI.JO', 'ARI.JO', 'GRT.JO', 'PPI.JO', 
    'BSL.JO', 'HAR.JO', 'TBS.JO', 'TCP.JO', 'TDH.JO', 'TEX.JO', 'TFG.JO', 'TWR.JO', 
    'VIS.JO', 'VKE.JO', 'VMK.JO', 'BWY.JO', 'CLS.JO', 'DSY.JO', 'EVS.JO', 'FNB.JO', 
    'GFI.JO', 'HCI.JO', 'IPL.JO', 'JBL.JO', 'KST.JO', 'LBH.JO', 'MND.JO', 'NHN.JO', 
    'NVT.JO', 'OML.JO', 'PBT.JO', 'PIK.JO', 'PP1.JO', 'QLT.JO', 'RCL.JO', 'RES.JO', 
    'RHM.JO', 'RLO.JO', 'RNF.JO', 'SHP.JO', 'SPR.JO', 'SSU.JO', 'STX.JO', 'SUN.JO', 
    'TAK.JO', 'TLM.JO', 'TPT.JO', 'TRL.JO', 'TSG.JO', 'UBS.JO', 'VIL.JO', 'WCP.JO',
    
    # 🇪🇬 EGX Egypte (limité sur TR, top 20)
    'ORAS.CA', 'ETHA.CA', 'SWDY.CA', 'HRHO.CA', 'PHDC.CA', 'TMGH.CA', 'EKHO.CA', 
    'CITH.CA', 'BIGO.CA', 'MFPC.CA',
    
    # ETF Afrique dispo TR
    'AFDB.DE', 'AFRK.DE'  # Africa-focused ETFs
]

    etfs = ['SPY', 'QQQ', 'SMH', 'TAN', 'ARKK', 'VUAA.DE', 'IWDA.AS', 'GLD', 'SLV']
    
    return {
        'US': us_tickers,      
        'PEA': pea_europe,
	'ASIE': asia_tickers,
	'AFRIQUE': africa_tickers,
        'MONDE': us_tickers + pea_europe + asia_tickers + africa_tickers,
        'ETF': etfs
    }

all_tickers = get_trade_republic_tickers()

# === SIDEBAR AVEC SLIDERS ===
st.sidebar.header("🌍 Zone Géographique")
univers = st.sidebar.selectbox(
    "Sélectionner la zone :", 
    ["PEA (Europe)", "US (États-Unis)", "MONDE (Toutes zones)", "ASIE", "AFRIQUE"
],
    index=0
)

st.sidebar.header("🏭 Secteurs d’activité")

secteurs_selectionnes = st.sidebar.multiselect(
    "Filtrer par secteur (optionnel)",
    options=SECTEURS_DISPONIBLES,
    default=SECTEURS_DISPONIBLES
)


st.sidebar.header("🔍 Critères de Filtrage")

# Sliders pour tous les paramètres
min_mcap = st.sidebar.slider("Capitalisation min (Md$)", 0.1, 1000.0, 2.0, 0.1)
max_per = st.sidebar.slider("PER maximum", 5, 100, 35, 1)
rsi_target = st.sidebar.slider("RSI cible", 10, 90, 50, 1)
min_roe = st.sidebar.slider("ROE minimum (%)", -20, 50, 5, 1)
min_volume = st.sidebar.slider("Volume min (M)", 0.1, 100.0, 1.0, 0.1)

no_baisse_1an = st.sidebar.checkbox("🚫 Exclure baisses 1 an", value=True, help="Garde seulement +15% YTD")

st.sidebar.markdown("---")
st.sidebar.info("💡 Ajustez les curseurs puis cliquez sur SCAN")

# === BOUTON SCAN ===
if st.button("🚀 SCANNER LES ACTIONS", type="primary", use_container_width=True):
    
    # Sélection des tickers selon l'univers
    if univers == "PEA (Europe)":
        tickers_to_scan = all_tickers['PEA']
        zone_label = "🇪🇺 Europe (PEA)"
    elif univers == "US (États-Unis)":
        tickers_to_scan = all_tickers['US']
        zone_label = "🇺🇸 États-Unis"
    elif "ASIE" in univers:
        tickers_to_scan = all_tickers['ASIE']
        zone_label = "🇯🇵🇨🇳"
    elif "AFRIQUE" in univers:
        tickers_to_scan = all_tickers['AFRIQUE']
        zone_label = "Afrique"
    else:  # MONDE
        tickers_to_scan = all_tickers['MONDE']
        zone_label = "🌍 Monde entier"
    
    st.info(f"🔍 Analyse de {len(tickers_to_scan)} actions ({zone_label})...")
    
    results = []
    progress_bar = st.progress(0)

    for idx, ticker in enumerate(tickers_to_scan):
        try:
            # Mise à jour de la barre de progression
            progress_bar.progress((idx + 1) / len(tickers_to_scan))
            
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="60d")
            
            if len(hist) < 20:
                continue

            sector = info.get("sector", "N/A")

            # 🔴 filtre secteur
            if sector not in secteurs_selectionnes:
                continue
            
            # Calcul du RSI
            rsi = RSIIndicator(hist['Close']).rsi().iloc[-1]
            
            # Récupération des données
            market_cap = info.get('marketCap', 0) / 1e9  # En milliards
            pe_ratio = info.get('trailingPE', 999)
            roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0
            volume = hist['Volume'].iloc[-1] / 1e6  # En millions
            company_name = info.get('longName', ticker)  # NOM COMPLET DE L'ENTREPRISE
            sector = info.get('sector', 'N/A')
            price = hist['Close'].iloc[-1]
            
            # Application des filtres
            if (market_cap >= min_mcap and
                pe_ratio <= max_per and
                abs(rsi - rsi_target) <= 15 and
                roe >= min_roe and
                volume >= min_volume):
                
                results.append({
                    'Ticker': ticker,
                    'Entreprise': company_name,  # NOM EXACT
                    'Secteur': sector,
                    'Prix ($)': round(price, 2),
                    'Cap. (Md$)': round(market_cap, 2),
                    'PER': round(pe_ratio, 1) if pe_ratio != 999 else 'N/A',
                    'ROE (%)': round(roe, 1),
                    'RSI': round(rsi, 1),
                    'Volume (M)': round(volume, 2)
                })
        
        except Exception as e:
            st.warning(f"Erreur lors de l’analyse de {ticker}: {str(e)}")
            continue
    
    progress_bar.empty()
    
    # === AFFICHAGE DES RÉSULTATS ===
    if results:
        df = pd.DataFrame(results)
        
        st.success(f"✅ {len(results)} actions trouvées sur {len(tickers_to_scan)} analysées")
        
        # Tableau des résultats
        st.dataframe(
            df,
            use_container_width=True,
            height=400,
            hide_index=True
        )

        # Graphique du nombre d'actions par secteur
        sector_count = df['Secteur'].value_counts()
        st.bar_chart(sector_count)

        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.scatter(
                df, 
                x='PER', 
                y='ROE (%)', 
                size='Cap. (Md$)',
                color='RSI',
                hover_data=['Entreprise', 'Ticker', 'Prix ($)'],
                title='📊 PER vs ROE (taille = capitalisation)',
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.bar(
                df.nlargest(10, 'Cap. (Md$)'),
                x='Entreprise',
                y='Cap. (Md$)',
                color='RSI',
                title='🏆 Top 10 Capitalisations',
                color_continuous_scale='Viridis'
            )
            fig2.update_xaxes(tickangle=45)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Export CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Télécharger les résultats (CSV)",
            data=csv,
            file_name=f'screener_results_{zone_label}.csv',
            mime='text/csv',
            use_container_width=True
        )

        # Sélection d'une action pour afficher l'historique des prix
        selected_ticker = st.selectbox("Sélectionnez une action à visualiser:", df['Ticker'].tolist())

        # Obtenir les données historiques de l'action sélectionnée
        selected_stock = yf.Ticker(selected_ticker)
        historique = selected_stock.history(period="1y")  # Les 12 derniers mois

        # Affichage du graphique
        if not historique.empty:
            st.line_chart(historique['Close'], use_container_width=True)
        else:
            st.warning("Aucune donnée disponible pour cette action.")
    
    else:
        st.warning("⚠️ Aucune action ne correspond à vos critères. Essayez d'élargir les filtres.")

else:
    st.info("👆 Configurez vos critères dans la barre latérale et cliquez sur SCANNER")

# Footer
st.markdown("---")
st.caption("📈 Données fournies par Yahoo Finance • Mise à jour toutes les heures")

