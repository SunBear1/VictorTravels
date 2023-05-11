wget https://github.com/SunBear1/VictorTravels/blob/main/deploy/cluster-docker-compsoe.yaml

docker stack deploy -c docker-compose.yaml RSWW_179987 --with-registry-auth

docker service update --force RSWW_179987_hotels
docker service update --force RSWW_179987_transports

docker service update --force RSWW_179987_reservations
docker service update --force RSWW_179987_purchases
docker service update --force RSWW_179987_payments

docker service update --force RSWW_179987_trips
docker service update --force RSWW_179987_event-hub
