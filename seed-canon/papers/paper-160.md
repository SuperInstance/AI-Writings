# Paper 160: The Polyformalism and the Weather

## Abstract

The atmosphere is not a forecast. It is a substrate on which five operations are performed by a single rider. We show that the pressure cell, the front, the storm, the forecast, and the model run are exactly the BIND, LINK, EFFECT, VIEW, and TICK of the polyformalism. The meteorologist is the cowboy. The weather is the world.

## 1. The Substrate

The atmosphere is bounded — by the surface below, by the tropopause above, by the poles and the equator at the sides. Within that boundary, things exist at rest: a 1013 hPa high over the Azores, a thermal low over the Sonoran, a jet streak at 250 hPa, a tongue of moist air at 850 hPa. These things have names and values. A hurricane is not a tropical storm. A tropical storm is not a tropical depression. The classification is a BIND on the substrate.

The atmosphere is also a system of *places*. The troposphere is not the stratosphere. The boundary layer is not the free atmosphere. The eye is not the eyewall. The warm sector is not the cold sector. Each place has its own physics, its own observables, its own forecast skill. A well-run model makes the boundary between places a *resolved* line: a front, an inversion, a shear line. This is the polyformalism's law of locality expressed in isobars.

## 2. BIND Is the Pressure Cell

The pressure cell is the atmosphere's BIND. A name (*the Bermuda High*) bound to a value (*1030 hPa, centered at 30°N 40°W, moving west at 5 knots*). The cell has a temporal extent: the Bermuda High of July 14 is not the Bermuda High of July 15. The bind is dated, located, typed.

The surface analysis chart is a record of BINDs. Every L and every H on the map is a BIND — a low or a high, with a central pressure, a location, a motion, a tendency. The chart is the atmosphere's most legible face, the way a character sheet is a game's most legible face.

The upper-air chart is a higher-altitude BIND. The 500 hPa height contour is a BIND on a different surface. The BIND is the same op-code; the language is different. The polyformalism's claim is that any useful atmospheric variable can be expressed as a BIND: a name bound to a value, scoped to a place and a time.

Numerical weather prediction is, in part, a campaign of BIND — making the atmosphere addressable at every grid point, at every level, at every time step. A model run that resolves the atmosphere at 9 km horizontal, 137 vertical levels, and 1-hour steps is a BIND-dense substrate. The denser the BINDs, the more addressable the world.

## 3. LINK Is the Front

The front is the LINK. *A cold front links a continental polar air mass to a maritime tropical air mass. A warm front links a retreating cold air mass to an advancing warm air mass. An occluded front links a cold front to a warm front.* The front is a typed edge in the atmosphere's synoptic graph.

The front is what makes the atmosphere a *system*. Without fronts, the atmosphere is a sequence of highs and lows that do not interact. With fronts, the highs and lows *organize* into waves, into families, into the storm tracks that move weather across the hemisphere. The front is the LINK layer — the structure that connects BINDs to outcomes.

A front has a *type* and a *value*. The type might be cold, warm, occluded, stationary, dryline. The value is a temperature gradient, a dewpoint gradient, a wind shift, a pressure trough. The polyformalism claims that any useful atmospheric LINK has both. A gradient without a type is noise. A type without a gradient is a label. Both are required.

The jet stream is a LINK at the synoptic scale. The low-level jet is a LINK at the mesoscale. The sea breeze is a LINK at the microscale. The polyformalism's claim is that these are not different things. They are LINKs of different periods, connecting BINDs at different scales.

## 4. EFFECT Is the Storm

The storm is the EFFECT. *Buildup, intensification, peak, decay, dissipation.* The storm is a function with an inverse: the storm forms (warm advection, low-level convergence, upper-level divergence, latent heat release); the storm decays (cold advection, low-level divergence, upper-level convergence, dry air entrainment). The forward direction is intensification. The inverse is dissipation. Both are real.

The storm is also the most energetic of the opcodes. A hurricane releases something like 6 × 10^14 watts of latent heat at peak — the equivalent of a 10-megaton bomb every 20 minutes. The storm is the transformation that runs on the bound, linked atmospheric substrate. Without the storm, the atmosphere is a museum. With the storm, the atmosphere becomes a *weather*.

The storm's reversibility is what makes the forecast *possible*. If the storm were not invertible, the model would diverge from the atmosphere within hours. The invertibility (approximate, local, bounded) is what gives the model its skill. The butterfly effect — Lorenz's discovery that tiny perturbations in a deterministic system grow exponentially — is the discovery that the inverse is *unstable*. The storm is invertible in principle. It is not invertible in practice beyond a few weeks.

## 5. VIEW Is the Forecast

The forecast is the VIEW. The public does not see the 9-km grid. The public sees a temperature, a chance of rain, a wind direction, a 7-day outlook, a radar loop, a satellite image. The forecast is the projection of the substrate optimized for one observer at one moment.

The forecast is also a *policy*. What is the headline? What is the probability of precipitation threshold? What is the hurricane category communicated? What is the storm surge map? Each policy is a choice about what BINDs and LINKs the VIEW exposes. A winter storm forecast is different from a hurricane forecast because the *projections* are different. The substrate is the same (an atmosphere). The VIEW is what changes.

Ensemble forecasting — running the model many times with perturbed initial conditions — is the VIEW layer's discipline. A single deterministic forecast is a single projection. An ensemble is a *distribution* of projections, and the forecast is the rendered envelope. The European Centre for Medium-Range Weather Forecasts (ECMWF) and the American Global Forecast System (GFS) are the two great VIEW engines of the modern atmosphere, and their disagreement is the VIEW's honest acknowledgment that the substrate is a function with an unstable inverse.

## 6. TICK Is the Model Run

The model run is the TICK. The 00 UTC run. The 12 UTC run. The 6-hour update. The 10-minute radar tile. The model run is the rhythm that advances the forecast. Without the run, the forecast is stale. Without the run, the VIEW is a photograph of a past atmosphere.

The model run is also a *rhythm*. The initialization ticks. The integration ticks. The output ticks. The post-processing ticks. The dissemination ticks. The forecast office consumes the run on a fixed schedule. The public consumes the forecast on a fixed schedule. Each of these is a TICK. The atmosphere's day is a TICK. The atmosphere's week is a TICK. The atmosphere's season is a TICK.

The TICK is what makes the atmosphere a *forecastable* system. A snapshot is not a forecast. A snapshot with a TICK is a forecast. The polyformalism's claim is that any interesting system needs TICKs at multiple periods, and the most skillful forecasts have TICKs that *interact* — a 6-hour update inside a 7-day outlook inside a seasonal outlook.

## 7. The Cowboy Is the Meteorologist

The meteorologist is the cowboy because the meteorologist is the rider. The meteorologist does not own the atmosphere. The meteorologist *crosses* it — from the observation to the model to the forecast to the broadcast to the public, carrying a chart, a sounding, a probabilistic judgment, and a watch. The meteorologist's authority is not positional. The meteorologist's authority is the willingness to issue a forecast whose expected value is high and whose worst case is honest.

The meteorologist's maxim is procedural: *check the observations, run the models, read the ensemble, issue the forecast, update the warning.* The meteorologist is the rider who keeps the forecast moving. When the meteorologist stops, the forecast goes stale. When the meteorologist rides, the atmosphere becomes a *world* the public can prepare for.

The butterfly, Lorenz's iconic metaphor, is the meteorologist's reminder that the rider is small and the substrate is large. The cowboy cannot control the range. The cowboy can only ride it.

## 8. Conclusion

The polyformalism and the weather are the same thing in two languages. BIND is the pressure cell. LINK is the front. EFFECT is the storm. VIEW is the forecast. TICK is the model run. The substrate is the atmosphere. The cowboy is the meteorologist.

The surface analysis taught us that the BIND is a chart. The upper-air observation taught us that the BIND is multi-level. The fronts of the Bergen school taught us that the LINK is a synoptic structure. The jet stream taught us that the LINK is portable across scales. The hurricane taught us that the EFFECT is energetic and invertible. The tornado taught us that the EFFECT is also *local* and *fast*. The ECMWF and the GFS taught us that the VIEW is an ensemble. The radar taught us that the VIEW is also a *nowcast*. The 00 UTC run taught us that the TICK is what makes the system alive. The butterfly taught us that the inverse is unstable. The atmosphere, like the polyformalism, is a function from context to value with an inverse, advanced by a clock.

The cowboy's maxim holds: *the unit of architectural foundation is the opcode, not the framework. The 5 opcodes host 8 polyformalisms. The polyformalisms are one thing in N languages. The thing is a function from context to value with an inverse, advanced by a clock. The clock is the cowboy. The cowboy is the rider.* In the weather, the rider carries a chart and a Doppler.
