CREATE TABLE custom_exceptions (
    id SERIAL PRIMARY KEY,
    exception_name VARCHAR(255) NOT NULL,
    exception_message TEXT NOT NULL,
    exception_code INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE exception_logs (
    id SERIAL PRIMARY KEY,
    exception_id INTEGER NOT NULL,
    log_message TEXT NOT NULL,
    log_level VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (exception_id) REFERENCES custom_exceptions(id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_exceptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    exception_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (exception_id) REFERENCES custom_exceptions(id)
);

INSERT INTO custom_exceptions (exception_name, exception_message, exception_code) 
VALUES ('InvalidUsername', 'Invalid username', 1001),
       ('InvalidEmail', 'Invalid email', 1002),
       ('InvalidPassword', 'Invalid password', 1003),
       ('UserNotFound', 'User not found', 1004),
       ('ExceptionNotFound', 'Exception not found', 1005);

CREATE OR REPLACE FUNCTION raise_custom_exception(p_exception_name VARCHAR, p_exception_message TEXT, p_exception_code INTEGER)
RETURNS VOID AS $$
BEGIN
    INSERT INTO custom_exceptions (exception_name, exception_message, exception_code) 
    VALUES (p_exception_name, p_exception_message, p_exception_code);
    RAISE EXCEPTION 'Custom exception raised: %', p_exception_message;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION log_exception(p_exception_id INTEGER, p_log_message TEXT, p_log_level VARCHAR)
RETURNS VOID AS $$
BEGIN
    INSERT INTO exception_logs (exception_id, log_message, log_level) 
    VALUES (p_exception_id, p_log_message, p_log_level);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION handle_user_exception(p_user_id INTEGER, p_exception_id INTEGER)
RETURNS VOID AS $$
BEGIN
    INSERT INTO user_exceptions (user_id, exception_id) 
    VALUES (p_user_id, p_exception_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_user_exceptions(p_user_id INTEGER)
RETURNS SETOF custom_exceptions AS $$
BEGIN
    RETURN QUERY 
    SELECT ce.* 
    FROM custom_exceptions ce 
    JOIN user_exceptions ue ON ce.id = ue.exception_id 
    WHERE ue.user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_exception_logs(p_exception_id INTEGER)
RETURNS SETOF exception_logs AS $$
BEGIN
    RETURN QUERY 
    SELECT el.* 
    FROM exception_logs el 
    WHERE el.exception_id = p_exception_id;
END;
$$ LANGUAGE plpgsql;