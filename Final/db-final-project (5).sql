
CREATE TABLE [Airline] (
	AirlineId int NOT NULL identity(1,1),
	AirlineName nvarchar(255) NOT NULL,
	ContactPerson nvarchar(255) NOT NULL,
	Phone nvarchar(255) NOT NULL,
	Email nvarchar(255) NOT NULL UNIQUE,
	HeadquarterCity nvarchar(255) NOT NULL,
	HeadquarterCountry nvarchar(255) NOT NULL,
  CONSTRAINT [PK_AIRLINE] PRIMARY KEY CLUSTERED
  (
  [AirlineId] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [Aircraft] (
	TailNumber int NOT NULL identity(1,1),
	Name nvarchar(255) NOT NULL,
	AircraftTypeID int NOT NULL,
	Capacity int NOT NULL,
	AirlineId int NOT NULL,
  CONSTRAINT [PK_AIRCRAFT] PRIMARY KEY CLUSTERED
  (
  [TailNumber] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [Runway] (
	RunwayId int NOT NULL identity(1,1),
	RunwayNumber int NOT NULL,
	RunwayLength int NOT NULL,
  CONSTRAINT [PK_RUNWAY] PRIMARY KEY CLUSTERED
  (
  [RunwayId] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [Termial] (
	TerminalId int NOT NULL identity(1,1),
	TerminalNumber nvarchar(255) NOT NULL,
  CONSTRAINT [PK_TERMIAL] PRIMARY KEY CLUSTERED
  (
  [TerminalId] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [Flights] (
	FlightID int NOT NULL identity(1,1),
	FlightNo int NOT NULL,
	Date date NOT NULL,
	Time time NOT NULL,
	TailNumber int NOT NULL,
	FlightStatus nvarchar(255) NOT NULL,
	RumwayID int NOT NULL,
	TerminalID int NOT NULL,
	DestinationTo int NOT NULL,
	ArrivalFrom int NOT NULL,
	FlightTypeID int NOT NULL,
	GateID int NOT NULL,
	IsDomestic bit,
  CONSTRAINT [PK_FLIGHTS] PRIMARY KEY CLUSTERED
  (
  [FlightID] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [AircraftType] (
	AircraftTypeID int NOT NULL identity(1,1),
	NameOfAircraft nvarchar(255) NOT NULL,
  CONSTRAINT [PK_AIRCRAFTTYPE] PRIMARY KEY CLUSTERED
  (
  [AircraftTypeID] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [FlightStatusTable] (
	FlightStatudID int NOT NULL identity(1,1),
	FlightStatus nvarchar(255) NOT NULL UNIQUE,
  CONSTRAINT [PK_FLIGHTSTATUSTABLE] PRIMARY KEY CLUSTERED
  (
  [FlightStatudID] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [FlightType] (
	TypeID int NOT NULL identity(1,1),
	TypeName nvarchar(255) NOT NULL,
  CONSTRAINT [PK_FLIGHTTYPE] PRIMARY KEY CLUSTERED
  (
  [TypeID] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [Gate] (
	GateID int NOT NULL identity(1,1),
	GateName nvarchar(255) NOT NULL,
  CONSTRAINT [PK_GATE] PRIMARY KEY CLUSTERED
  (
  [GateID] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [Airports] (
	AirportID int NOT NULL identity(1,1),
	AirportName nvarchar(255) NOT NULL,
	City nvarchar(255) NOT NULL,
	Country nvarchar(255) NOT NULL,
  CONSTRAINT [PK_AIRPORTS] PRIMARY KEY CLUSTERED
  (
  [AirportID] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [User] (
	id int NOT NULL identity(1,1),
	username varchar(255) NOT NULL,
	password varchar(255) NOT NULL,
	UserTypeId int NOT NULL,
  CONSTRAINT [PK_USER] PRIMARY KEY CLUSTERED
  (
  [id] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [UserType] (
	UserTypeId int NOT NULL identity(1,1),
	Type varchar(255) NOT NULL,
  CONSTRAINT [PK_USERTYPE] PRIMARY KEY CLUSTERED
  (
  [UserTypeId] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [Country] (
	CountryID int NOT NULL identity(1,1),
	CountryName varchar(255) NOT NULL,
  CONSTRAINT [PK_COUNTRY] PRIMARY KEY CLUSTERED
  (
  [CountryID] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO
CREATE TABLE [City] (
	CityID int NOT NULL identity(1,1),
	CountryID int NOT NULL,
	CityName varchar(255) NOT NULL,
  CONSTRAINT [PK_CITY] PRIMARY KEY CLUSTERED
  (
  [CityID] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO

ALTER TABLE [Aircraft] WITH CHECK ADD CONSTRAINT [Aircraft_fk0] FOREIGN KEY ([AircraftTypeID]) REFERENCES [AircraftType]([AircraftTypeID])

GO
ALTER TABLE [Aircraft] CHECK CONSTRAINT [Aircraft_fk0]
GO
ALTER TABLE [Aircraft] WITH CHECK ADD CONSTRAINT [Aircraft_fk1] FOREIGN KEY ([AirlineId]) REFERENCES [Airline]([AirlineId])

GO
ALTER TABLE [Aircraft] CHECK CONSTRAINT [Aircraft_fk1]
GO



ALTER TABLE [Flights] WITH CHECK ADD CONSTRAINT [Flights_fk0] FOREIGN KEY ([TailNumber]) REFERENCES [Aircraft]([TailNumber])

GO
ALTER TABLE [Flights] CHECK CONSTRAINT [Flights_fk0]
GO
ALTER TABLE [Flights] WITH CHECK ADD CONSTRAINT [Flights_fk1] FOREIGN KEY ([FlightStatus]) REFERENCES [FlightStatusTable]([FlightStatus])

GO
ALTER TABLE [Flights] CHECK CONSTRAINT [Flights_fk1]
GO
ALTER TABLE [Flights] WITH CHECK ADD CONSTRAINT [Flights_fk2] FOREIGN KEY ([RumwayID]) REFERENCES [Runway]([RunwayId])

GO
ALTER TABLE [Flights] CHECK CONSTRAINT [Flights_fk2]
GO
ALTER TABLE [Flights] WITH CHECK ADD CONSTRAINT [Flights_fk3] FOREIGN KEY ([TerminalID]) REFERENCES [Termial]([TerminalId])

GO
ALTER TABLE [Flights] CHECK CONSTRAINT [Flights_fk3]
GO
ALTER TABLE [Flights] WITH CHECK ADD CONSTRAINT [Flights_fk4] FOREIGN KEY ([DestinationTo]) REFERENCES [Airports]([AirportID])

GO
ALTER TABLE [Flights] CHECK CONSTRAINT [Flights_fk4]
GO
ALTER TABLE [Flights] WITH CHECK ADD CONSTRAINT [Flights_fk5] FOREIGN KEY ([ArrivalFrom]) REFERENCES [Airports]([AirportID])

GO
ALTER TABLE [Flights] CHECK CONSTRAINT [Flights_fk5]
GO
ALTER TABLE [Flights] WITH CHECK ADD CONSTRAINT [Flights_fk6] FOREIGN KEY ([FlightTypeID]) REFERENCES [FlightType]([TypeID])

GO
ALTER TABLE [Flights] CHECK CONSTRAINT [Flights_fk6]
GO
ALTER TABLE [Flights] WITH CHECK ADD CONSTRAINT [Flights_fk7] FOREIGN KEY ([GateID]) REFERENCES [Gate]([GateID])

GO
ALTER TABLE [Flights] CHECK CONSTRAINT [Flights_fk7]
GO






ALTER TABLE [User] WITH CHECK ADD CONSTRAINT [User_fk0] FOREIGN KEY ([UserTypeId]) REFERENCES [UserType]([UserTypeId])

GO
ALTER TABLE [User] CHECK CONSTRAINT [User_fk0]
GO



ALTER TABLE [City] WITH CHECK ADD CONSTRAINT [City_fk0] FOREIGN KEY ([CountryID]) REFERENCES [Country]([CountryID])

GO
ALTER TABLE [City] CHECK CONSTRAINT [City_fk0]
GO

