create schema abc;
CREATE TABLE abc.company_information (
  company_id bigint not null primary key not null,
  company_size varchar(50) not null,
  last_session date not null DEFAULT CURRENT_TIMESTAMP,
  created_at date not null DEFAULT CURRENT_TIMESTAMP
);
create index "ci_company_id_idx" on abc.company_information(company_id);
CREATE TABLE abc.session_information (
  session_id bigint NOT null primary KEY,
  created_at date not null DEFAULT CURRENT_TIMESTAMP,
  company_id bigint NOT null,
  CONSTRAINT FK_COMPANY_INFO FOREIGN KEY (company_id) REFERENCES abc.company_information (company_id) ON DELETE CASCADE
);
create index "session_delete_cascade_idx" on abc.session_information(company_id, session_id);
create index "company_id_idx" on abc.session_information(company_id);
create index "session_id_idx" on abc.session_information(session_id);