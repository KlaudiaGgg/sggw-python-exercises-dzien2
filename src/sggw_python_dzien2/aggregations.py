# Ćwiczenie 5


from sqlalchemy import select, func
from sqlalchemy.orm import Session

from sggw_python_dzien2.database import engine, Experiment, DataPoint


# Pobieranie sumy i średniej dla każdego eksperymentu
stmt = (
    select(
        Experiment.title,
        func.sum(DataPoint.real_value),
        func.avg(DataPoint.real_value),
        func.sum(DataPoint.target_value),
        func.avg(DataPoint.target_value)
    )
    .join(DataPoint)
    .group_by(Experiment.id, Experiment.title)
)


with Session(engine) as session:
    results = session.execute(stmt)

    for row in results:
        print(f"\n{row[0]}")
        print(f"Suma real_value: {row[1]}")
        print(f"Średnia real_value: {row[2]}")
        print(f"Suma target_value: {row[3]}")
        print(f"Średnia target_value: {row[4]}")
