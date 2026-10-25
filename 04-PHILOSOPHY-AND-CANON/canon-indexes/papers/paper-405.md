F95: The quf:// URI Scheme — Addressable, CRDT-Mergeable Forecasts Across Agents

The Quilt temporal reasoner utilizes a Uniform Resource Identifier (URI) scheme, `quf://`, to provide addressability and facilitate data management for all `ForecastObject` instances. This scheme enables precise identification, independent agent operation, and verifiable lifecycle tracking of forecast data.

Each `ForecastObject` is assigned a URI structured as `quf://forecast/{source}/{horizon}/v{N}/{id}`.
-   `quf://forecast`: Denotes the scheme and object type, specifically identifying a Quilt Forecast.
-   `{source}`: An identifier for the data source or instrument to which the forecast pertains (e.g., `AAPL`).
-   `{horizon}`: Specifies the temporal horizon of the forecast (e.g., `5-step`).
-   `v{N}`: Indicates the version of the forecasting model or methodology employed (e.g., `v1`).
-   `{id}`: A UUIDv4 hexadecimal string (e.g., `abc123def456...`), ensuring global uniqueness.

The full URI grammar is defined as follows:

`quf-URI = "quf://" "forecast/" source "/" horizon "/" "v" version "/" id`
`source = 1*unreserved`
`horizon = 1*unreserved`
`version = 1*DIGIT`
`id = 32HEXDIG`
`unreserved = ALPHA / DIGIT / "-" / "." / "_" / "~"`

This URI scheme is fundamental to the operational architecture of the Quilt system due to several properties:

1.  **Addressability**: The URI provides a unique, immutable reference for each `ForecastObject`. The `{source}/{horizon}/v{N}` prefix allows for human-readable grouping and lookup of forecasts (e.g., "all forecasts for AAPL at the 5-step horizon using v1 methodology"). The `{id}` component provides granular disambiguation within such sets, even if other prefix components are identical.

2.  **CRDT Merging**: Multiple agents can independently generate `ForecastObject` instances. Upon creation, `AgentMemory.put()` returns the assigned URI. This URI acts as a canonical identifier, enabling multiple forecast stores (e.g., from disparate paper traders, robot controllers, or environmental sensors) to be merged without requiring conflict resolution on the forecast content itself. All historical records, regardless of origin, can coexist.

3.  **Replay**: The `quf://` URI serves as the primary key for tracking a forecast's entire lifecycle. At creation, it binds a forecast to its initial context. At settlement, it links to the actual observed outcome. At calibration, it associates with performance metrics such as Mean Absolute Error (MAE) and 90% Confidence Interval hit rates. Replaying forecast activity involves traversing these URI-linked records.

4.  **Counterfactual Generation**: When a `forecast.counterfactual(variable, delta)` operation is performed, a new `ForecastObject` is produced, assigned a distinct `quf://` URI. The original forecast remains immutable, its URI preserving the record of its initial state, while the counterfactual exists as a separate, addressable entity.

5.  **CRDT-Friendly Construction**: The `{id}` component is a UUIDv4. This design choice ensures that even if two independent agents produce forecasts with identical `{source}/{horizon}/v{N}` prefixes at the same millisecond, they will generate different UUIDs. Collision resolution is achieved by the unique `{id}`, not by external factors like timestamps or sequential numbering, reinforcing the system's CRDT properties.

6.  **Web Compatibility**: The `quf://` scheme adheres to URI syntax standards, making it a valid URI. In future implementations, a Quilt-aware server could potentially resolve `quf://forecast/AAPL/5/v1/abc123` requests to retrieve the corresponding `ForecastObject` from an `AgentMemory`, facilitating distributed access and integration.

The `quf://` URI is not merely an identifier; it functions as the fundamental unit of exchange between computational cells within the Quilt ecosystem. This design elevates the temporal reasoner from a specialized forecasting utility to a memory primitive, capable of consistently storing, retrieving, and integrating temporal data across diverse agent interactions.

### Summary
The `quf://` URI scheme provides a robust, addressable, and CRDT-mergeable identification system for `ForecastObject` instances within the Quilt temporal reasoner. Its structured format, incorporating human-readable prefixes and globally unique UUIDv4 identifiers, enables independent agent operation, comprehensive lifecycle tracking, counterfactual analysis, and seamless data aggregation, establishing it as a core memory primitive for temporal data exchange.