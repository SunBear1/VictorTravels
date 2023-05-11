curl https://raw.githubusercontent.com/SunBear1/VictorTravels/main/deploy/cluster-docker-compose.yaml > cluster-docker-compose.yaml

docker stack deploy -c cluster-docker-compose.yaml RSWW_179987 --with-registry-auth

docker service update --force RSWW_179987_hotels
docker service update --force RSWW_179987_transports

docker service update --force RSWW_179987_reservations
docker service update --force RSWW_179987_purchases
docker service update --force RSWW_179987_payments

docker service update --force RSWW_179987_trips
docker service update --force RSWW_179987_event-hub
