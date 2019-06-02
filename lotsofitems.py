# This file populates the database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie

"""
SQLAlchemy executes CRUD operations via an interface called a session
Sessions allow us to write down all commands we want to execute but not
send to the database until calling a commit

Use these to begin interpeter queries:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

This gives us a staging zone for all the objects loaded into the DBSession
object

Any change made to the objects in the session won't be persisted into the
database until we call session.commit()

Some Categories:
Action
Adventure
Comedy
Drama
Fantasy
Horry
Mystery
Romance
Science Fiction
Thriller

CREATE
Syntax for making a New Entry (Genre)
>>> new_entry = ClassName(property='value', ...)
>>> session.add(new_entry)
>>> session.commit()

Add an Movie
>>> alien = Movie(name='Alien', description='A 1979 film directed by Ridley
... Scott, it follows the crew of the commercial space tug Nostromo who
... encounter the eponymous Alien, a deadly and aggressive extraterrestrial
... set loose on the ship.', genre=first_genre)
>>> session.add(alien)
>>> session.commit()

READ
Use the Session to Interact with the Database
We can check that a new entry was added by using

>>> session.query(Category).all()
[<database_setup.Category object at 0x10d4aeef0>]

This goes into the database and finds the table that corresponds to the
Category class and finds all the entries in the table and returns them in a
list

Check that the Movie was added
>>> session.query(Movie).all()
[<database_setup.Movie object at 0x10e47c400>]

UPDATE
If we want to edit anything we can query the database for a specific item

The .one() at the end makes sure SQLAlchemy only gives the one object we want
instead of a list we have to iterate over

>>> alien = session.query(Movie).filter_by(id=1).one()

Just to check
>>> alien.name
'Alien'
>>> alien.id
1
>>> alien.description
'A 1979 film directed by Ridley Scott, it follows the crew of the commercial
 space tug Nostromo who encounter the eponymous Alien, a deadly and aggressive
 extraterrestrial set loose on the ship'
>>> alien.description = 'A 1979 film directed by Ridley Scott, it follows the
... crew of the commercial space tug Nostromo who encounter the eponymous
... alien, a deadly and aggressive extraterrestrial set loose on the ship'
>>> session.add(alien)
>>> session.commit()

To check the change was made

>>> alien = session.query(Movie).filter_by(id=1).one()
>>> alien.description
'A 1979 film directed by Ridley Scott, it follows the crew of the commercial
 space tug Nostromo who encounter the eponymous alien, a deadly and aggressive
 extraterrestrial set loose on the ship'

DELETE
In order to delete from our database, we want to query for the object we want
to delete, delete it, then commit the session

>>> schindler = session.query(Movie).filter_by(name="Schindler's List").one()
>>> session.delete(schindler)
>>> session.commit()

Now we can search again to see if the movie was deleted

>>> schindler = session.query(Movie).filter_by(name="Schindler's List").one()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/lib/python3.7/site-packages/sqlalchemy/orm/query.py",
    line 3282, in one
    raise orm_exc.NoResultFound("No row was found for one()")
sqlalchemy.orm.exc.NoResultFound: No row was found for one()

"""

# This lets program know which database to communicate with
engine = create_engine('sqlite:///catalog.db')
# This binds the engine to the Base class which makes the connection between
# the class definitions and their corresponding tables within the database
Base.metadata.bind = engine
# Establish a link between code executions and the engine
DBSession = sessionmaker(bind=engine)
# This gives a staging zone for all objects loaded into DBSession object
session = DBSession()

# The Action Genre and Alien (as Action) has been added to the database
# Add the rest of the genres and some movies as part of those genres

# Action Genre
action = Genre(name="Action")
session.add(action)
session.commit()

# Action Movies
alien = Movie(name="Alien",
    description=("A 1979 film directed by Ridley Scott, it follows the crew"
                 " of the commercial space tug Nostromo who encounter the"
                 " eponymous Alien, a deadly and aggressive extraterrestrial"
                 " set loose on the ship"),
    genre=action)
session.add(alien)
session.commit()

die_hard = Movie(name="Die Hard",
    description=("A 1988 film directed by John McTiernan that follows"
                " off-duty New York City Police Department officer John"
                " McClane (Bruce Willis) who is caught in a Los Angeles"
                " skyscraper during a heist led by Hans Gruber (Alan Rickman)"),
    genre=action)
session.add(die_hard)
session.commit()

predator = Movie(name="Predator",
    description=("A 1987 film directed by John McTiernan that follows an"
                " elite military rescue team on a mission to save hostages"
                " in guerrilla-held territory in Central America. The"
                " Predator, a technologically advanced space alien, stalks"
                " and hunts the main characters"),
    genre=action)
session.add(predator)
session.commit()

matrix = Movie(name="The Matrix",
    description=("A 1999 film directed by the Wachowskis, it depicts a"
                  " dystopian future in which humanity is unknowingly"
                  " trapped inside a simulated reality, the Matrix, created"
                  " by thought-capable machines to distract humans while"
                  " using their bodies as an energy source"),
    genre=action)
session.add(matrix)
session.commit()

gladiator = Movie(name="Gladiator",
    description=("A 2000 film directed by Ridley Scott that follows general"
                " Maximus Decimus Meridius, who is betrayed when Commodus,"
                " the ambitious son of Emperor Marcus Aurelius, murders his"
                " father and seizes the throne"),
    genre=action)
session.add(gladiator)
session.commit()

print("Action movies added!")

# Adventure Genre
adventure = Genre(name="Adventure")
session.add(adventure)
session.commit()

print("Adventure genre added!")

# Adventure Movies
kong = Movie(name="Kong: Skull Island",
    description=("A 2017 film directed by Jordan Vogt-Roberts that is a reboot"
                " of the King Kong franchise"),
    genre=adventure)
session.add(kong)
session.commit()

captain_america = Movie(name="Captain America: The First Avenger",
    description=("A 2011 film based on the Marvel Comics character Captain"
                " America. The film tells the story of Steve Rogers, a man"
                " from Brooklyn who is transformed into the super-soldier"
                " Captain America and must stop the Red Skull, who intends"
                " to use an artifact called the 'Tesseract' as a source for"
                " world domination"),
    genre=adventure)
session.add(captain_america)
session.commit()

avengers = Movie(name="The Avengers",
    description=("A 2012 film based on the Marvel Comics superhero team of"
                " the same name.  In the film, Nick Fury, director of the"
                " spy agency S.H.I.E.L.D., recruits Tony Stark, Steve Rogers,"
                " Bruce Banner, and Thor to form a team that must stop Thor's"
                " brother Loki from subjugating Earth"),
    genre=adventure)
session.add(avengers)
session.commit()

guardians = Movie(name="Guardians of the Galaxy",
    description=("A 2014 film based on the Marvel Comics superhero team of"
                  " the same name. In the film, Peter Quill forms an uneasy"
                  " alliance with a group of extraterrestrial criminals who"
                  " are on the run after stealing a powerful artifact"),
    genre=adventure)
session.add(guardians)
session.commit()

doctor_strange = Movie(name="Doctor Strange",
    description=("A 2016 film based on the Marvel Comics character of the"
                " same name. In the film, former surgeon Stephen Strange"
                " learns the mystic arts after a career-ending car crash"),
    genre=adventure)
session.add(doctor_strange)
session.commit()

print("Adventure movies added!")

# Comedy Genre
comedy = Genre(name="Comedy")
session.add(comedy)
session.commit()

print("Comedy genre added!")

# Comedy Movies
jump_street = Movie(name="21 Jump Street",
    description=("A 2012 film directed by Phil Lord and Christopher Miller,"
                " it follows two police officers who are forced to relive"
                " high school when they are assigned to go undercover as"
                " high school students to prevent the outbreak of a new"
                " synthetic drug and arrest its supplier"),
    genre=comedy)
session.add(jump_street)
session.commit()

bridesmaids = Movie(name="Bridesmaids",
    description=("A 2011 film directed by Paul Feig, it centers on Annie"
                " (Kristen Wiig), who suffers a series of misfortunes after"
                " being asked to serve as maid of honor for her best friend,"
                " Lillian (Maya Rudolph)"),
    genre=comedy)
session.add(bridesmaids)
session.commit()

hangover = Movie(name="The Hangover",
    description=("A 2009 film directed by Todd Phillips, it tells the story of"
                " Phil Wenneck, Stu Price, Alan Garner, and Doug Billings,"
                " who travel to Las Vegas for a bachelor party to celebrate"
                " Doug's impending marriage"),
    genre=comedy)
session.add(hangover)
session.commit()

step_brothers = Movie(name="Step Brothers",
    description=("A 2008 film directed by Adam Mckay, it follows Brennan"
                " (Will Ferrell) and Dale (John C. Reilly), two grown men who"
                " are forced to live together as brothers after their single"
                " parents marry each other"),
    genre=comedy)
session.add(step_brothers)
session.commit()

tropic_thunder = Movie(name="Tropic Thunder",
    description=("A 2008 film directed by Ben Stiller, it follows a group of"
                " prima donna actors who, when their frustrated director"
                " (Steve Coogan) drops them in the middle of a jungle, are"
                " forced to rely on their acting skills to survive the real"
                " action and danger"),
    genre=comedy)
session.add(tropic_thunder)
session.commit()

print("Comedy movies added!")

# Drama Genre
drama = Genre(name="Drama")
session.add(drama)
session.commit()

print("Drama genre added!")

# Drama Movies
first_man = Movie(name="First Man",
    description=("A 2018 film directed by Damien Chazelle that follows the"
                " years leading up to the Apollo 11 mission to the Moon"
                " in 1969"),
    genre=drama)
session.add(first_man)
session.commit()

true_story = Movie(name="True Story",
    description=("A 2015 film directed by Rupert Goold, it follows the story"
                " of Christian Longo, a man on the FBI's most wanted list"
                " accused of murdering his wife and three children in Oregon."
                " He hid in Mexico using the identity of journalist"
                " Michael Finkel"),
    genre=drama)
session.add(true_story)
session.commit()

help = Movie(name="The Help",
    description=("A 2011 film directed by Tate Taylor, it recounts the story"
                 " of aspiring journalist Eugenia. The story focuses on her"
                 " relationship with two black maids, Aibileen and Minny,"
                 " during the Civil Rights Movement in 1963"
                 " Jackson, Mississippi"),
    genre=drama)
session.add(help)
session.commit()

schindler = Movie(name="Schindler's List",
    description=("A 1993 film directed by Steven Spielberg, it follows Oskar"
                 " Schindler, a Sudeten German businessman, who saved the"
                 " lives of more than a thousand mostly Polish-Jewish"
                 " refugees from the Holocaust by employing them in his"
                 " factories during World War II"),
    genre=drama)
session.add(schindler)
session.commit()

shawhank = Movie(name="The Shawshank Redemption",
    description=("A 1994 film directed by Frank Darabont, it tells the story"
                 " of banker Andy Dufresne, who is sentenced to life in"
                 " Shawshank State Penitentiary for the murder of his wife"
                 " and her lover, despite his claims of innocence"),
    genre=drama)
session.add(shawhank)
session.commit()

print("Drama movies added!")

# Fantasy Genre
fantasy = Genre(name="Fantasy")
session.add(adventure)
session.commit()

print("Fantasy genre added!")

# Fantasy Movies
fantastic_beasts = Movie(name="Fantastic Beasts and Where to Find Them",
    description=("A 2016 film directed by David Yates, it is a spin-off and"
                 " prequel to the Harry Potter film series, and is produced"
                 " and written by J. K. Rowling, inspired by her 2001 guide"
                 " book of the same name"),
    genre=fantasy)
session.add(fantastic_beasts)
session.commit()

hobbit = Movie(name="The Hobbit: An Unexpected Journey",
    description=("A 2012 film directed by Peter Jackson, tells the tale of"
                 " Bilbo Baggins, who is convinced by the wizard Gandalf to"
                 " accompany thirteen Dwarves, led by Thorin Oakenshield, on"
                 " a quest to reclaim the Lonely Mountain from the"
                 " dragon Smaug"),
    genre=fantasy)
session.add(hobbit)
session.commit()

harry_potter = Movie(name="Harry Potter and the Deathly Hallows: Part 2",
    description=("A 2011 film directed by David Yates, the film continues"
                 " to follow Harry Potter's quest to find and destroy Lord"
                 " Voldemort's Horcruxes in order to stop him once and"
                 " for all"),
    genre=fantasy)
session.add(harry_potter)
session.commit()

print("Fantasy movies added!")

# Horror Genre
horror = Genre(name="Horror")
session.add(adventure)
session.commit()

print("Horror genre added!")

# Horror Movies
us = Movie(name="Us",
    description=("A 2019 film directed by Jordan Peele, it follows a family"
                 " who are confronted by murderous doppelgangers known as"
                 " 'the Tethered'"),
    genre=horror)
session.add(us)
session.commit()

it = Movie(name="It",
    description=("A 2017 film directed by Andrés Muschietti, it tells the"
                 " story of seven children in Derry, Maine, who are"
                 " terrorized by the eponymous being, only to face their"
                 " own personal demons in the process"),
    genre=horror)
session.add(it)
session.commit()

get_out = Movie(name="Get Out",
    description=("A 2017 film directed by Jordan Peele, it follows Chris"
                 " Washington, a young African-American man who uncovers"
                 " a disturbing secret when he meets the family of"
                 " his Caucasian girlfriend"),
    genre=horror)
session.add(get_out)
session.commit()

print("Horror movies added!")

# Mystery Genre
mystery = Genre(name="Mystery")
session.add(adventure)
session.commit()

print("Mystery genre added!")

# Mystery Movies
zodiac = Movie(name="Zodiac",
    description=("A 2007 film directed by David Fincher, it tells the story"
                 " of the manhunt for the Zodiac Killer, a serial killer who"
                 " called himself the 'Zodiac' and killed in and around the"
                 " San Francisco Bay Area during the late 1960s and"
                 " early 1970s"),
    genre=mystery)
session.add(zodiac)
session.commit()

shutter = Movie(name="Shutter Island",
    description=("A 2010 film directed by Martin Scorsese, U.S. Marshal"
                 " Edward 'Teddy' Daniels is investigating a psychiatric"
                 " facility on Shutter Island after one of the patients"
                 " goes missing"),
    genre=mystery)
session.add(shutter)
session.commit()

seven = Movie(name="Seven",
    description=("A 1995 film directed by David Fincher, it tells the story"
                 " of David Mills, a detective who partners with the"
                 " retiring William Somerset to track down a serial killer"
                 " who uses the seven deadly sins as a motif in his murders"),
    genre=mystery)
session.add(seven)
session.commit()

print("Mystery movies added!")

# Romance Genre
romance = Genre(name="Romance")
session.add(adventure)
session.commit()

print("Romance genre added!")

# Romance Movies
notebook = Movie(name="The Notebook",
    description=("A 2004 film directed by Nick Cassavetes, the film stars"
                 " Ryan Gosling and Rachel McAdams as a young couple who "
                 "fall in love in the 1940s"),
    genre=romance)
session.add(notebook)
session.commit()

valentines = Movie(name="Valentine's Day",
    description=("A 2010 film directed by Garry Marshall, the film follows"
                 " a group of related characters and their struggles with"
                 " love on Valentine's Day"),
    genre=romance)
session.add(valentines)
session.commit()

proposal = Movie(name="The Proposal",
    description=("A 2009 film directed by Anne Fletcher, it centers on a"
                 " Canadian executive who learns that she may face"
                 " deportation from the U.S. because of her expired visa."
                 " Determined to stay, she convinces her assistant to act as"
                 " her fiancé"),
    genre=romance)
session.add(proposal)
session.commit()

print("Romance movies added!")

# Science Fiction Genre
science_fiction = Genre(name="Science Fiction")
session.add(adventure)
session.commit()

print("Science Fiction genre added!")

# Science Fiction Movies
arrival = Movie(name="Arrival",
    description=("A 2016 film directed by Denis Villeneuve, the  film"
                 " follows a linguist enlisted by the U.S. Army to discover"
                 " how to communicate with aliens who have arrived on Earth,"
                 " before tensions lead to war"),
    genre=science_fiction)
session.add(arrival)
session.commit()

interstellar = Movie(name="Interstellar",
    description=("A 2014 film directed by Christopher Nolan, the film follows"
                 " a group of astronauts who travel through a wormhole near"
                 " Saturn in search of a new home for humanity"),
    genre=science_fiction)
session.add(interstellar)
session.commit()

inception = Movie(name="Inception",
    description=("A 2010 film directed by Christopher Nolan, the film follows"
                 " a professional thief who steals information by infiltrating"
                 " the subconscious"),
    genre=science_fiction)
session.add(inception)
session.commit()

print("Science Fiction movies added!")

# Thriller Genre
thriller = Genre(name="Thriller")
session.add(thriller)
session.commit()

print("Thriller genre added!")

# Thriller Movies
lambs = Movie(name="The Silence of the Lambs",
    description=("A 1991 film directed by Jonathan Demme, it follows Clarice"
                 " Starling, a young FBI trainee, who seeks the advice of"
                 " imprisoned Dr. Hannibal Lecter, a brilliant psychiatrist"
                 " and cannibalistic serial killer to apprehend another"
                 " serial killer"),
    genre=thriller)
session.add(lambs)
session.commit()

searching = Movie(name="Searching",
    description=("A 2018 film directed by Aneesh Chaganty, set entirely on"
                 " computer screens and smartphones, the film follows a"
                 " father trying to find his missing 16-year-old daughter"
                 " with the help of a police detective"),
    genre=thriller)
session.add(searching)
session.commit()

gone_girl = Movie(name="Gone Girl",
    description=("A 2014 film directed by David Fincher, the story begins as"
                 " a mystery that follows the events surrounding Nick Dunne,"
                 " who becomes the primary suspect in the sudden disappearance"
                 " of his wife Amy"),
    genre=thriller)
session.add(gone_girl)
session.commit()

print("Thriller movies added!")
