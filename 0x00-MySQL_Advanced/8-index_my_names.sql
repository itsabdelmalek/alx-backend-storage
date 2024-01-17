-- Creates an index idx_name_first on the table 'names' for the first letter of the 'name' column
CREATE INDEX idx_name_first
 ON names(name(1));
