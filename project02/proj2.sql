
create table 
   (cust_no varchar(80)	not null unique,
    customer_name	varchar(255)	not null,
    customer_city 	varchar(30)	not null,
    constraint pk_customer primary key(customer_name));