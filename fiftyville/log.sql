-- Keep a log of any SQL queries you execute as you solve the mystery.
sqlite3 fiftyville.db

-- July 28, 2021

SELECT id, description
FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28
AND street = 'Humphrey Street'
-- | 295 | Theft at 10:15am.
-- Interview with 3 witnesses who were present at the time, all mention bakery

SELECT *
FROM interviews
WHERE transcript LIKE '%bakery%'

-- {A1 -- thief drove off in car within 10 min of theft

-- A2 -- Leggett Street ATM 28/07 morning, thief withdraw money

-- A3 -- as thief was leaving bakery, they alled someone, less than 1min,
-- A3 -- plan to take earliest flight tmr
-- A3 -- thief asked the other person to buy flight ticket}

-- A1

SELECT id as ID, name as NAME, phone_number as PHONE, passport_number as PASS
FROM people
WHERE people.license_plate IN
(
    SELECT license_plate as LICENSE
    FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28
    AND hour = 10 AND minute >= 15 AND minute <= 25
    AND activity = 'exit'
)
-- A1 -- license_plate: 5P2BI95, 94KL13X, 6P58WS2,
--                      4328GD8, G412CB7, L93JTIZ,
--                      322W7JE, 0NTHK55.

-- A2


SELECT person_id
FROM bank_accounts
WHERE account_number IN
(
    SELECT account_number
    FROM atm_transactions
    WHERE year = 2021 AND month = 7 AND day = 28
    AND atm_location = 'Leggett Street'
    AND transaction_type = 'withdraw'
)

AND person_id IN
(
    SELECT id
    FROM people
    WHERE people.license_plate IN
    (
        SELECT license_plate as LICENSE
        FROM bakery_security_logs
        WHERE year = 2021 AND month = 7 AND day = 28
        AND hour = 10 AND minute >= 15 AND minute <= 25
        AND activity = 'exit'
    )
)
-- A2 -- peron_id: 686048, 514354, 396669, 467400

SELECT name, phone_number, passport_number
FROM people
WHERE id = 686048 OR id = 514354 OR id = 396669 OR id = 467400


-- A3
SELECT *
FROM airports
WHERE city = 'Fiftyville'
-- airport id = 8


SELECT id, destination_airport_id, hour, minute
FROM flights
WHERE year = 2021 AND month = 7 AND day = 29
AND origin_airport_id = 8
-- earliest flight is to destination airport id = 4, flight id = 36

SELECT *
FROM airports
WHERE id = 4
-- Destination: LaGuardia Airport (LGA), New York City

SELECT *
FROM passengers
WHERE flight_id = 36
AND passport_number IN
(
    SELECT passport_number
    FROM people
    WHERE id = 686048 OR id = 514354 OR id = 396669 OR id = 467400
)
 -- Bruce or Luca

SELECT*
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28
AND duration <= 60
AND caller IN
(
    SELECT phone_number
    FROM people
    WHERE name = 'Bruce' OR name = 'Luca'
)

SELECT name, phone_number
FROM people
WHERE name = 'Bruce' OR name = 'Luca'

-- Caller is Bruce

SELECT *
FROM people
WHERE phone_number = '(375) 555-8161'

-- Accomplice is Robin