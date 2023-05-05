package com.cringe.travels.trips.trip.entity;

import lombok.AllArgsConstructor;
import lombok.Data;


@Data
@AllArgsConstructor
public class Transport {
    private TransportDetails plane;
    private TransportDetails train;
    private TransportDetails own;
}
