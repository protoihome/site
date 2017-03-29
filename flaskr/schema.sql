drop table if exists rooms;
create table rooms (
	id integer primary key autoincrement,
	name text not null,
	'descricao' text not null
);
drop table if exists devices;
create table devices (
	id integer primary key autoincrement,
	name text not null,
	id_rooms integer not null,
	'description' text,
	FOREIGN KEY(id_rooms) REFERENCES rooms(id)
);