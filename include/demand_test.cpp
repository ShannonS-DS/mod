
#include <iostream>
#include <random>
#include "demand.hpp"

using namespace std;

void test_query(mod::DemandLookup& dl) {
    mod::GeoLocation p_st(-73.991788392187516, -73.991788392187516);
    mod::GeoLocation d_st(-73.78195999999997,-73.78195999999997);
    double prob = dl.query_demand(0, 2, p_st, d_st);

    cout << "==================== Query Test ====================" << endl;
    cout << "Probability -> " << prob << endl << endl;
}

void test_sample(mod::DemandLookup& dl) {
    const int num = 10;
    vector<mod::Demand> dems;
    mod::Time st(2, 0), end(10, 10);
    dl.sample(num, st, end, dems);

    cout << "==================== Sample Test ====================" << endl;
    cout << "Sampling " << num << " Demands" << endl;
    for (int i = 0; i < num; i++) {
        cout << "\t" << dems[i] << endl;
    }
    cout << endl;
}

int main() {
    srand(time(NULL));
    mod::DemandLookup dl("../data/trip_data_5_stations_short.csv",
            "../data/trip_data_5_probs_short.csv",
            "../data/trip_data_5_times_short.csv");
    test_query(dl);
    test_sample(dl);
}
