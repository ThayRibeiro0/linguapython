SELECT *
FROM   people
WHERE  license_plate  IN
       (
              SELECT license_plate
              FROM   bakery_security_logs
              WHERE  month = 7
              AND    day = 28
              AND    year = 2021
              AND    hour = 10
              AND    minute BETWEEN 15 AND    26)
AND    people.id IN
       (
              SELECT person_id
              FROM   bank_accounts
              JOIN   people
              JOIN   atm_transactions
              ON     atm_transactions.account_number = bank_accounts.account_number
              WHERE  atm_transactions.month = 7
              AND    atm_transactions.day = 28
              AND    atm_transactions.year = 2021
              AND    transaction_type = "withdraw"
              AND    atm_transactions.atm_location = "Leggett Street"
              AND    people.phone_number IN
                     (
                            SELECT caller
                            FROM   phone_calls
                            WHERE  month = 7
                            AND    day = 29
                            AND    year = 2021
                            AND    duration < 60)
              AND    people.passport_number IN
                     (
                            SELECT passport_number
                            FROM   passengers
                            WHERE  flight_id IN
                                   (
                                            SELECT   id
                                            FROM     flights
                                            WHERE    month = 7
                                            AND      day = 29
                                            AND      year = 2021
                                            ORDER BY hour,
                                                     minute ASC limit 1)));
