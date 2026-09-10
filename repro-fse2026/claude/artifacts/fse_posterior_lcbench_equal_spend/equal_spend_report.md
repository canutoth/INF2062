# Equal-measured-spend comparison (LCBench)

Same protocol as the ENERGY equal-spend experiment; LCBench is the
weak cost-target-coupling case (cost = runtime, target = accuracy),
testing the mechanism prediction that pilotCost's equal-spend penalty
shrinks or disappears when the outcome-relevant information is not
concentrated in the expensive tail.

Scopes (dataset x budget level): 140.
pilotCost beats random at equal spend in 84/140 scopes (median affordable-n multiplier 1.66x; capped in 0 scopes).
SRS beats random at equal spend in 46/140 scopes.

Equal-spend winners:

- `diversity`: 80/140
- `balanced`: 27/140
- `pairwise`: 15/140
- `SRSSampling`: 12/140
- `pilotCost`: 6/140
