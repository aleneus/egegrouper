"""
EGEGrouper - Software for grouping electrogastroenterography examinations.

Copyright (C) 2017 Aleksandr Popov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

# create new SME data base 
create_sme_db = """
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
"""

# import SME data base
add_sme_db = """
-- Create temporary table for variables and store max values of SMEP entities from nation db.
drop table if exists variable;
create table variable(name text primary key, value integer);
insert into variable(name, value) values('max_exam_id', (select coalesce(max(exam_id),0) from examination));
insert into variable(name, value) values('max_meas_id', (select coalesce(max(meas_id),0) from measurement));
insert into variable(name, value) values('max_group_id', (select coalesce(max(group_id),0) from egeg_group));

-- Paste groups with increased id to onation DB from source DB
insert into egeg_group(group_id, name, description) select group_id + (select value from variable where name = 'max_group_id'), name, description from source.egeg_group;

-- Paste examinations
insert into examination(exam_id, name, diagnosis, age, gender) select exam_id + (select value from variable where name = 'max_exam_id'), name, diagnosis,age,gender from source.examination;

-- Paste measurements
insert into measurement(meas_id, time, exam_id) select meas_id + (select value from variable where name = 'max_meas_id'), time, exam_id + (select value from variable where name = 'max_exam_id') from source.measurement;

-- Paste signals
insert into signal(data, dt, meas_id, edited) select data, dt, meas_id + (select value from variable where name = 'max_meas_id'), edited from source.signal;

-- Connect SMEP and groups
insert into group_element(exam_id, group_id) select exam_id+(select value from variable where name = 'max_exam_id'), group_id + (select value from variable where name = 'max_group_id') from source.group_element;
"""
