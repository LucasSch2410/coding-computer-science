-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Looking a crime scene
SELECT description
FROM crime_scene_reports
WHERE day = 28 AND month = 7 AND street = 'Humphrey Street';

-- Checking interview
SELECT transcript
FROM interviews
WHERE day = 28 AND month = 7 AND transcript LIKE '%bakery%';

-- Searches into bakery security logs
SELECT *
FROM bakery_security_logs
WHERE day = 28 AND month = 7 AND hour = 10 AND minute BETWEEN 15 AND 25;

-- Searches all the people that are drive away from the bakery
SELECT * from people
WHERE license_plate in
(SELECT license_plate
FROM bakery_security_logs
WHERE day = 28 AND month = 7 AND hour = 10 AND minute BETWEEN 15 AND 25);

-- Searches all the phone calls less than 60 seconds.
SELECT * FROM phone_calls
WHERE duration <= 60
AND month = 7
AND day = 28;

-- Searches all the withdraws
SELECT * FROM atm_transactions
WHERE day = 28
AND month = 7
AND transaction_type = 'withdraw'
AND atm_location = 'Leggett Street';

-- Searches the most recently flight
SELECT * FROM flights
WHERE origin_airport_id = 8
AND month = 7 AND day = 29
ORDER BY hour, minute
LIMIT 1;


-- Searches phone calls
SELECT * FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE duration <= 60
AND month = 7
AND day = 28
AND caller in
    (SELECT phone_number from people
    WHERE license_plate in
        (SELECT license_plate
        FROM bakery_security_logs
        WHERE day = 28 AND month = 7 AND hour = 10 AND minute BETWEEN 15 AND 25));

-- The passenger with the description. (Bruce)
SELECT name FROM passengers
JOIN flights ON passengers.flight_id = flights.id
JOIN people ON passengers.passport_number = people.passport_number
WHERE people.passport_number in
    (SELECT passport_number FROM people
    JOIN phone_calls ON people.phone_number = phone_calls.caller
    WHERE duration <= 60
    AND month = 7
    AND day = 28
    AND caller in
        (SELECT phone_number from people
        WHERE license_plate in
            (SELECT license_plate
            FROM bakery_security_logs
            WHERE day = 28 AND month = 7 AND hour = 10 AND minute BETWEEN 15 AND 25)))
AND flight_id in
    (SELECT id FROM flights
    WHERE origin_airport_id = 8
    AND month = 7 AND day = 29
    ORDER BY hour, minute
    LIMIT 1)
AND people.id in
    (SELECT person_id FROM bank_accounts
    WHERE account_number in
        (SELECT account_number FROM atm_transactions
        WHERE day = 28
        AND month = 7
        AND transaction_type = 'withdraw'
        AND atm_location = 'Leggett Street'));




-- Searches the partner (Robin)
SELECT name FROM phone_calls
JOIN people ON phone_calls.receiver = people.phone_number
WHERE duration <= 60
AND day = 28
AND caller =
(SELECT phone_number FROM passengers
JOIN flights ON passengers.flight_id = flights.id
JOIN people ON passengers.passport_number = people.passport_number
WHERE people.passport_number in
    (SELECT passport_number FROM people
    JOIN phone_calls ON people.phone_number = phone_calls.caller
    WHERE duration <= 60
    AND month = 7
    AND day = 28
    AND caller in
        (SELECT phone_number from people
        WHERE license_plate in
            (SELECT license_plate
            FROM bakery_security_logs
            WHERE day = 28 AND month = 7 AND hour = 10 AND minute BETWEEN 15 AND 25)))
AND flight_id in
    (SELECT id FROM flights
    WHERE origin_airport_id = 8
    AND month = 7 AND day = 29
    ORDER BY hour, minute
    LIMIT 1)
AND people.id in
    (SELECT person_id FROM bank_accounts
    WHERE account_number in
        (SELECT account_number FROM atm_transactions
        WHERE day = 28
        AND month = 7
        AND transaction_type = 'withdraw'
        AND atm_location = 'Leggett Street')));


-- Searches the city destination (New York City)

SELECT city FROM airports
WHERE id =
    (SELECT destination_airport_id FROM passengers
    JOIN flights ON passengers.flight_id = flights.id
    JOIN people ON passengers.passport_number = people.passport_number
    WHERE people.passport_number in
        (SELECT passport_number FROM people
        JOIN phone_calls ON people.phone_number = phone_calls.caller
        WHERE duration <= 60
        AND month = 7
        AND day = 28
        AND caller in
            (SELECT phone_number from people
            WHERE license_plate in
                (SELECT license_plate
                FROM bakery_security_logs
                WHERE day = 28 AND month = 7 AND hour = 10 AND minute BETWEEN 15 AND 25)))
    AND flight_id in
        (SELECT id FROM flights
        WHERE origin_airport_id = 8
        AND month = 7 AND day = 29
        ORDER BY hour, minute
        LIMIT 1)
    AND people.id in
        (SELECT person_id FROM bank_accounts
        WHERE account_number in
            (SELECT account_number FROM atm_transactions
            WHERE day = 28
            AND month = 7
            AND transaction_type = 'withdraw'
            AND atm_location = 'Leggett Street')));
