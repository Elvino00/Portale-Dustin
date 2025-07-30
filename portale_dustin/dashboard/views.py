from django.shortcuts import render , get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Device
from dashboard.queries import CrateDBQueries
from django.conf import settings
from datetime import datetime
import pandas as pd
import plotly.express as px
# Create your views here.

@login_required(login_url='autenticazione:login')
def home(request):
    veicoli = Device.objects.all().order_by('nome_veicolo')
    return render(request, 'dashboard/home.html', {
        'user': request.user,
        'veicoli': veicoli
    })



def dettaglio_veicolo(request, id_device):
    # Recupera il dispositivo
    device = get_object_or_404(Device, id_device=id_device)
    
    # Parametri fissi per il test (stessi della dashboard_view)
    start_date_str = "18-07-2025"
    end_date_str = "21-07-2025"
    intervallo_minuti = 10

    # Lista parametri ECG
    ecg_params = [
        'bpm',
        'hrv_sdnn',
        'hrv_rmssd',
        'hrv_prc80nn',
        'hrv_medianNN',
        'hrv_pNN20',
        'hrv_meanNN',
        'hrv_prc20nn'
    ]

    try:
        # Conversione date
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y")
        
        if end_date < start_date:
            return render(request, 'dashboard/dettaglio_veicolo.html', {
                'device': device,
                'error': "La data finale deve essere successiva a quella iniziale"
            })

        ts_start = int(start_date.timestamp())
        ts_end = int(end_date.timestamp())

    except ValueError:
        return render(request, 'dashboard/dettaglio_veicolo.html', {
            'device': device,
            'error': "Formato date non valido. Usare DD-MM-YYYY (es. 18-07-2025)"
        })

    if (ts_end - ts_start) < 60:
        return render(request, 'dashboard/dettaglio_veicolo.html', {
            'device': device,
            'error': "L'intervallo temporale deve essere di almeno 1 minuto"
        })

    try:
       
        data = CrateDBQueries.get_some_ecg_statistics(ts_start, ts_end)
        
        if not data:
            return render(request, 'dashboard/dettaglio_veicolo.html', {
                'device': device,
                'error': "Nessun dato ECG trovato per questo veicolo nell'intervallo selezionato"
            })

        # Creazione DataFrame
        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'], unit='s')

        # Campionamento dati
        if intervallo_minuti > 1:
            df = (df.set_index('time')
                .resample(f'{intervallo_minuti}T')
                .first()
                .reset_index()
                .dropna())

        # Verifica parametri disponibili
        available_params = [p for p in ecg_params if p in df.columns]
        
        if not available_params:
            return render(request, 'dashboard/dettaglio_veicolo.html', {
                'device': device,
                'error': "Nessun parametro ECG valido trovato nei dati"
            })

        # Creazione grafico
        fig = px.line(df, x='time', y=available_params,
                    title=f'Statistiche ECG dal {start_date_str} al {end_date_str}',
                    labels={'value': 'Valore', 'time': 'Data/Ora', 'variable': 'Parametro'},
                    template='plotly_white',
                    color_discrete_sequence=px.colors.qualitative.Plotly)

        # Personalizzazione grafico (come nella dashboard_view)
        fig.update_layout(
            xaxis=dict(
                tickformat='%d-%m %H:%M',
                tickmode='auto',
                nticks=min(20, len(df)),
                rangeslider=dict(visible=True)
            ),
            yaxis=dict(fixedrange=False),
            hovermode="x unified",
            legend=dict(
                title_text='Parametri',
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                itemsizing='constant'
            ),
            margin=dict(l=50, r=50, b=100, t=100, pad=4),
            height=600
        )

        # Converti il grafico in HTML
        graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

        return render(request, 'dashboard/dettaglio_veicolo.html', {
            'device': device,
            'graph_html': graph_html,
            'start_date': start_date_str,
            'end_date': end_date_str
        })

    except Exception as e:
        if settings.DEBUG:
            import traceback
            traceback.print_exc()
        return render(request, 'dashboard/dettaglio_veicolo.html', {
            'device': device,
            'error': f"Errore durante la generazione del grafico: {str(e)}"
        })