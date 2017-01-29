pragma foreign_keys=1;

create table signal(
	signal_id integer,
	data blob,
	dt real,
	edited integer, 
	meas_id integer references measurement(meas_id) on delete cascade, 
	primary key(signal_id)
);

create table measurement(
	meas_id integer, 
	time text, 
	exam_id integer references examination(exam_id) on delete cascade, 
	primary key(meas_id)
);

create table examination(
	exam_id integer, 
	name text,
	diagnosis text, 
	age integer, 
	gender text, 
	primary key(exam_id)
);

create table egeg_group(
	group_id integer, 
	name text, 
	description text,
	primary key(group_id)		
);

create table group_element(
	exam_id integer references examination(exam_id) on delete cascade, 
	group_id integer references egeg_group(group_id) on delete cascade, 
	primary key(exam_id, group_id)
);
