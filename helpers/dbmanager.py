from extras import *

@debug
def calendarioOrdenado(dbpath: str) -> list[dict]:
    with sql.connect(dbpath) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Events ORDER BY Año, Mes, Día, Inicio, Final")
        raw = cursor.fetchall()
        db.commit()
    raw = [{head:info for head, info in zip(header, eventTuple)} for eventTuple in raw]
    data = []
    for event in raw:
        event["Inicio"] = intToStrDate(event["Inicio"])
        event["Final"] = intToStrDate(event["Final"])
        data.append(event)
    return data

@debug
def getCalendarioFromDB(dbpath: str) -> list[dict]:
    with sql.connect(dbpath) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Events")
        raw = cursor.fetchall()
        db.commit()
    raw = [{head:info for head, info in zip(header, eventTuple)} for eventTuple in raw]
    data = []
    for event in raw:
        event["Inicio"] = intToStrDate(event["Inicio"])
        event["Final"] = intToStrDate(event["Final"])
        data.append(event)
    return data

@debug
def putEventInDB(event: dict, dbpath: str) -> bool:
    try:
        with sql.connect(dbpath) as db:
            cursor = db.cursor()
            cursor.execute(f"INSERT INTO Events VALUES {tuple(event.values())}")
            db.commit()
        return True
    except: return False

@debug
def removeEventFromDB(event: dict, dbpath: str) -> bool:
    try:
        with sql.connect(dbpath) as db:
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM Events WHERE ({parseToSQLParams(event, ' AND ')})")
            db.commit()
        return True
    except: return False

@debug
def actualizarDB(dbpath: str) -> None:
    now = datetime.datetime.now()
    with sql.connect(dbpath) as db:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM Events WHERE Año < {now.year} OR (Año = {now.year} AND (Mes < {now.month} OR (Mes = {now.month} AND Día < {now.day})))")
        db.commit()