from .crate_client import crate_db
from typing import List, Dict, Any, Optional

class CrateDBQueries:
    @staticmethod
    def get_sensor_data(sensor_type: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Recupera i dati di un sensore specifico"""
        query = """
            SELECT * 
            FROM "mtopeniot"."etcar" 
            WHERE sensor = :sensor_type
            LIMIT :limit
        """
        return crate_db.execute_query(query, {
            'sensor_type': sensor_type,
            'limit': limit
        })

    @staticmethod
    def get_time_range_data(entity_id: str, start_time: int, end_time: int) -> List[Dict[str, Any]]:
        """Recupera i dati per un entity_id in un range temporale"""
        query = """
            SELECT * 
            FROM "mtopeniot"."etcar" 
            WHERE entity_id = :entity_id 
            AND time_index BETWEEN :start_time AND :end_time
            ORDER BY time_index
        """
        return crate_db.execute_query(query, {
            'entity_id': entity_id,
            'start_time': start_time,
            'end_time': end_time
        })

    @staticmethod
    def get_sensor_stats(sensor_type: str, json_field: Optional[str] = None) -> Dict[str, Any]:
        """Recupera statistiche per un sensore, eventualmente su un campo specifico del JSON"""
        if json_field:
            query = """
                SELECT 
                    MIN(CAST(data_json[:json_field] AS DOUBLE)) as min_val,
                    MAX(CAST(data_json[:json_field] AS DOUBLE)) as max_val,
                    AVG(CAST(data_json[:json_field] AS DOUBLE)) as avg_val
                FROM "mtopeniot"."etcar"
                WHERE sensor = :sensor_type
            """
            params = {
                'sensor_type': sensor_type,
                'json_field': json_field
            }
        else:
            query = """
                SELECT 
                    COUNT(*) as count,
                    MIN(time_index) as first_record,
                    MAX(time_index) as last_record
                FROM "mtopeniot"."etcar"
                WHERE sensor = :sensor_type
            """
            params = {'sensor_type': sensor_type}
        
        results = crate_db.execute_query(query, params)
        return results[0] if results else {}

    @staticmethod
    def get_ecg_bpm_values(limit: int = 100) -> List[Dict[str, Any]]:
        """Recupera i valori BPM dai dati ECG"""
        query = """
            SELECT 
                entity_id,
                time_index,
                CAST(data_json['BPM'] AS INTEGER) as bpm
            FROM "mtopeniot"."etcar"
            WHERE sensor = 'ecg'
            LIMIT :limit
        """
        return crate_db.execute_query(query, {'limit': limit})

    @staticmethod
    def get_stress_predictions(threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Recupera le predizioni di stress con confidence sopra una soglia"""
        query = """
            SELECT 
                entity_id,
                time_index,
                CAST(data_json['prediction'] AS INTEGER) as prediction,
                CAST(data_json['confidence'] AS DOUBLE) as confidence
            FROM "mtopeniot"."etcar"
            WHERE sensor = 'stress'
            AND CAST(data_json['confidence'] AS DOUBLE) > :threshold
            ORDER BY confidence DESC
        """
        return crate_db.execute_query(query, {'threshold': threshold})
    
    @staticmethod
    def get_some_ecg_statistics() -> List[Dict[str, Any]]:
        query = """SELECT
            ts_ms * 1000      AS "time",   
            CAST(data_json['BPM'] AS INTEGER) as BPM,
            CAST(data_json['HRV_SDNN'] AS DOUBLE) as HRV_SDNN,
            CAST(data_json['HRV_prc80NN'] AS DOUBLE) as HRV_prc80NN,
            CAST(data_json['HRV_medianNN'] AS DOUBLE) as HRV_medianNN,
            CAST(data_json['HRV_pNN20'] AS DOUBLE) as HRV_pNN20,
            CAST(data_json['HRV_meanNN'] AS DOUBLE) as HRV_meanNN,
            CAST(data_json['HRV_RMSSD'] AS DOUBLE) as HRV_RMSSD,
            CAST(data_json['HRV_prc20NN'] AS DOUBLE) as HRV_prc20NN
            
            FROM "mtclient_1"."etblackbox"
            WHERE sensor    = 'ecg'
            AND entity_id = 'urn:ngsi-ld:Bb:01'
            AND ts_ms     >= 1752451200    
            AND ts_ms     <= 1752710400
            ORDER BY ts_ms
        """
        return crate_db.execute_query(query)


# Esempi di utilizzo:
# if __name__ == "__main__":
#     # 1. Recupera dati ECG
#     ecg_data = CrateDBQueries.get_sensor_data('ecg', limit=5)
#     print("Dati ECG:", ecg_data)
    
#     # 2. Recupera statistiche per EDA
#     eda_stats = CrateDBQueries.get_sensor_stats('eda', 'SCR_mean')
#     print("Statistiche EDA:", eda_stats)
    
#     # 3. Recupera dati in un range temporale
#     time_data = CrateDBQueries.get_time_range_data(
#         'urn:ngsi-ld:Bb:01', 
#         1752505163602, 
#         1752585460930
#     )
#     print("Dati temporali:", len(time_data), "record trovati")
    
#     # 4. Recupera valori BPM
#     bpm_values = CrateDBQueries.get_ecg_bpm_values(10)
#     print("Valori BPM:", bpm_values)
    
#     # 5. Recupera predizioni di stress
#     stress_data = CrateDBQueries.get_stress_predictions(0.6)
#     print("Predizioni di stress:", stress_data)