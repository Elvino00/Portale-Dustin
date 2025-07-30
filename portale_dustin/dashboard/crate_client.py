# Importa il modulo SQLAlchemy con alias 'sa' per comodità
import sqlalchemy as sa
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from typing import Optional, List, Dict, Any

# Definizione della classe CrateDBClient che implementa il pattern Singleton
class CrateDBClient:
    # Variabile di classe per memorizzare l'unica istanza del Singleton
    _instance: Optional['CrateDBClient'] = None
    
    # Variabile di classe per memorizzare l'engine di connessione al database
    _engine: Optional[Engine] = None
    
    # Variabile di classe per la factory che crea sessioni
    _session_factory: Optional[scoped_session] = None

    # Metodo speciale __new__ che controlla la creazione dell'istanza
    def __new__(cls) -> 'CrateDBClient':
        # Verifica se esiste già un'istanza
        if cls._instance is None:
            # Se non esiste, crea una nuova istanza
            cls._instance = super(CrateDBClient, cls).__new__(cls)
            # Inizializza la connessione al database
            cls._initialize()
        # Restituisce sempre la stessa istanza
        return cls._instance

    # Metodo di classe per l'inizializzazione della connessione
    @classmethod
    def _initialize(cls) -> None:
        """Inizializza la connessione al database"""
        # Stringa di connessione per CrateDB (formato: crate://host:port)
        dburi = "crate://localhost:4200"
        
        # Crea l'engine SQLAlchemy con:
        # - pool_pre_ping=True per verificare la connessione prima dell'uso
        cls._engine = sa.create_engine(dburi, pool_pre_ping=True)
        
        # Crea una session factory con scoped_session che:
        # - Gestisce automaticamente lo scope delle sessioni
        # - Si assicura che la stessa sessione venga riutilizzata nello stesso thread
        cls._session_factory = scoped_session(
            sessionmaker(bind=cls._engine)  # Crea sessioni collegate all'engine
        )

    # Property per accedere alle sessioni
    @property
    def session(self) -> scoped_session:
        """Restituisce una nuova sessione"""
        if self._session_factory is None:
            raise RuntimeError("Session factory not initialized. Call _initialize() first.")
        # Restituisce una nuova sessione dalla factory
        return self._session_factory()

    # Metodo di classe per eseguire query
    @classmethod
    def execute_query(cls, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Esegue una query e restituisce i risultati"""
        if cls._engine is None:
            raise RuntimeError("Database engine not initialized. Call _initialize() first.")
            
        try:
            # Apre una connessione dall'engine
            with cls._engine.connect() as connection:
                # Esegue la query:
                # - sa.text() converte la stringa in un oggetto query SQLAlchemy
                # - params sono i parametri opzionali per la query
                result = connection.execute(sa.text(query), params if params else {})
                rows = result.fetchall()
                
                # Converte ogni riga del risultato in un dizionario Python
                # result.mappings() restituisce righe come dizionari
                # dict(row) converte in un vero dizionario Python

                data_toreturn = [dict(row._mapping) for row in rows]

                connection.commit() 
                return data_toreturn
        except SQLAlchemyError as e:
            # Stampa l'errore a console 
            print(f"Database error: {str(e)}")
            # Rilancia l'eccezione per gestirla a livello superiore
            raise

    #funzione di debug
    @classmethod
    def explain_query(cls, query: str, params: Optional[Dict[str, Any]] = None):
        """Esegui EXPLAIN sulla query per vedere come viene interpretata"""
        if cls._engine is None:
            raise RuntimeError("Database engine not initialized. Call _initialize() first.")
        explain_query = f"EXPLAIN {query}"
        try:
            with cls._engine.connect() as connection:
                result = connection.execute(sa.text(explain_query), params or {})
                plan = result.fetchone()
                print("Execution Plan:\n", plan)
        except Exception as e:
            print(f"EXPLAIN error: {str(e)}")

# Crea un'istanza globale del client CrateDB
crate_db = CrateDBClient()