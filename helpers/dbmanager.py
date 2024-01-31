from extras import *

@logs
async def calendarioOrdenado(dbpath: str):
    with sql.connect(dbpath) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Events ORDER BY Año, Mes, Día, Inicio, Final")
        raw = cursor.fetchall()
        db.commit()
    raw = [{head:info for head, info in zip(header, eventTuple)} for eventTuple in raw]
    data = []
    for event in raw:
        event["Inicio"] = await intToStrDate(event["Inicio"])
        event["Final"] = await intToStrDate(event["Final"])
        data.append(event)
    return data

@logs
async def getCalendarioFromDB(dbpath: str) -> list[dict]:
    with sql.connect(dbpath) as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Events")
        raw = cursor.fetchall()
        db.commit()
    raw = [{head:info for head, info in zip(header, eventTuple)} for eventTuple in raw]
    data = []
    for event in raw:
        event["Inicio"] = await intToStrDate(event["Inicio"])
        event["Final"] = await intToStrDate(event["Final"])
        data.append(event)
    return data

@logs
async def putEventInDB(event: dict, dbpath: str) -> bool:
    try:
        with sql.connect(dbpath) as db:
            cursor = db.cursor()
            cursor.execute(f"INSERT INTO Events VALUES {tuple(event.values())}")
            db.commit()
        return True
    except: return False

@logs
async def removeEventFromDB(event: dict, dbpath: str) -> bool:
    try:
        with sql.connect(dbpath) as db:
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM Events WHERE ({await parseToSQLParams(event, ' AND ')})")
            db.commit()
        return True
    except: return False

@logs
async def actualizarDB(dbpath: str) -> None:
    now = datetime.datetime.now()
    print(now.year, now.month, now.day)
    with sql.connect(dbpath) as db:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM Events WHERE Año < {now.year} OR (Año = {now.year} AND (Mes < {now.month} OR (Mes = {now.month} AND Día < {now.day})))")
        db.commit()