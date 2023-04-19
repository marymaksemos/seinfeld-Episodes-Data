import csv
from sqlmodel import create_engine, Session, select, SQLModel, Field
from typing import List, Optional
from datetime import datetime


class Episode(SQLModel, table=True):
    episode: int = Field(primary_key=True)
    season: int
    episode_in_season: int
    title: str
    air_date: datetime
    opening_line: str

class Replik(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    season: int
    episode: int = Field(foreign_key="episode.episode",default=None)
    character: str
    line: str
     
class Director(SQLModel, table=True):
    name: str = Field(primary_key=True)
    

class Writer(SQLModel, table=True):
    name: str = Field(primary_key=True)

      
class Episodedirector(SQLModel, table=True):
    episode: int = Field(foreign_key="episode.episode", primary_key=True)
    director: str = Field(foreign_key="director.name", primary_key=True)
        
class EpisodeWriter(SQLModel, table=True):  
    episode: int = Field(foreign_key="episode.episode",primary_key=True)
    writer: str = Field(foreign_key="writer.name",primary_key=True)


if __name__ == "__main__":

    sqlite_file_name = "futurama.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url, echo=True)

    SQLModel.metadata.create_all(engine)

    # read and process csv data
    with open("episode_list.csv", encoding="latin-1") as file:
        lines = file.readlines()[1:]
    reader = csv.reader(lines)
    episodes = list(reader)
    for ep in episodes:
        try: 
            date = datetime.strptime(ep[6], "(%Y-%m-%d)") 
        except ValueError:  
            date = datetime.strptime(ep[6], "(%B %d, %Y)") 

        episode = Episode(
            season=int(ep[0]),
            episode=int(ep[1]),
            episode_in_season=int(ep[2]),
            title=ep[3],
            air_date=date,
            opening_line=ep[7],
        )

        episode_pk = int(ep[1])
        with Session(engine) as session:
            session.add(episode)
            session.commit()

        directors=[]
        directors = ep[4].split(" & ")
        for director in directors:
                d = session.exec(select(Director).where(Director.name == director)).first()
                if not d:
                    d = Director(name=director)
                    ed = Episodedirector(episode=episode_pk, director=d.name)
                    with Session(engine) as session:
                        session.add(d)
                        session.add(ed)
                        session.commit()

        writers = []
        if "," in ep[5]:
            w = ep[5]
            w = ep[5].replace(" and ", ",")
            writers = w.split(",")
        elif ":" in ep[5]:
            w = ep[5].split(":")[0]
            writers = [writer.strip() for writer in w.split(",")]
        elif "&" in ep[5]:
            writers = ep[5].split(" & ")
        else:
            writers = [ep[5]]

        for writer in writers:
            
                w = session.execute(select(Writer).where(Writer.name == writer)).first()
                if not w:
                    w = Writer(name=writer)
                    ew = EpisodeWriter(episode=episode_pk, writer=w.name)
                    with Session(engine) as session:
                        session.add(w)
                        session.add(ew)
                        session.commit()
                

    # read from only_spoken_test

    with open("only_spoken_text.csv", encoding="latin-1") as file:
        lines = file.readlines()[1:]
    reader = csv.reader(lines)
    repliks = list(reader)
    for replik in repliks:
        r = Replik(season=replik[0], episode=replik[1], character=replik[2], line=replik[3])
        with Session(engine) as session:
            session.add(r)
            session.commit()
