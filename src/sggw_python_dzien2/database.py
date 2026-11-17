# Ćwiczenie 2, 3 i 4 z 18.10.2026 


import random
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy import ForeignKey, select, update, delete
from sqlalchemy.orm import declarative_base, Session, relationship

from sqlalchemy import Table, ForeignKey


# Połączenie z bazą SQLite
engine = create_engine("sqlite:///experiments.db", echo=True)

# Klasa bazowa dla modeli
Base = declarative_base()
# Tabela pośrednicząca dla relacji wiele-do-wielu
subject_experiment = Table(
    "subject_experiment",
    Base.metadata,
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True),
    Column("experiment_id", Integer, ForeignKey("experiments.id"), primary_key=True)
)

# Tabela Experiment
class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    created_at = Column(DateTime)
    type = Column(Integer)
    finished = Column(Boolean, default=False)

    data_points = relationship("DataPoint", back_populates="experiment")

    subjects = relationship(
        "Subject",
        secondary=subject_experiment,
        back_populates="experiments"
)

# Tabela DataPoint
class DataPoint(Base):
    __tablename__ = "data_points"

    id = Column(Integer, primary_key=True)
    real_value = Column(Float)
    target_value = Column(Float)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))

    experiment = relationship("Experiment", back_populates="data_points")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    gdpr_accepted = Column(Boolean, default=False)

    experiments = relationship(
        "Experiment",
        secondary=subject_experiment,
        back_populates="subjects"
    )

# Tworzenie tabel
# Base.metadata.create_all(engine) #Zakomentowane w związku z zadaniem 5 - ALEMBIC


if __name__ == "__main__":

    with Session(engine) as session:

        # 1. Tworzenie dwóch eksperymentów
        experiment1 = Experiment(
            title="Eksperyment 1",
            created_at=datetime.now(),
            type=1
        )

        experiment2 = Experiment(
            title="Eksperyment 2",
            created_at=datetime.now(),
            type=2
        )

        # 2. Dodawanie 10 punktów do pierwszego eksperymentu
        for i in range(10):
            point = DataPoint(
                real_value=random.random(),
                target_value=random.random()
            )
            experiment1.data_points.append(point)

        # 3. Dodawanie 10 punktów do drugiego eksperymentu
        for i in range(10):
            point = DataPoint(
                real_value=random.random(),
                target_value=random.random()
            )
            experiment2.data_points.append(point)

        session.add_all([experiment1, experiment2])
        session.commit()

        print("\nDodano 2 eksperymenty i 20 punktów danych.")

        # 4. Pobieranie eksperymentów i ich punktów danych
        experiments = session.scalars(select(Experiment)).all()

        for experiment in experiments:
            print(f"\n{experiment.title}")
            print(f"ID: {experiment.id}")
            print(f"Data utworzenia: {experiment.created_at}")
            print(f"Typ: {experiment.type}")
            print(f"Zakończony: {experiment.finished}")
            print(f"Liczba punktów: {len(experiment.data_points)}")

            for point in experiment.data_points:
                print(
                    point.id,
                    point.real_value,
                    point.target_value
                )

        # 5. Aktualizacja wszystkich eksperymentów
        session.execute(
            update(Experiment).values(finished=True)
        )

        session.commit()

        print("\nWszystkie eksperymenty oznaczono jako zakończone.")

        # 6. Usuwanie rekordów - zakomentowane
        # session.execute(delete(DataPoint))
        # session.execute(delete(Experiment))
        # session.commit()

        # print("Usunięto wszystkie rekordy.")
