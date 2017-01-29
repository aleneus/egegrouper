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

