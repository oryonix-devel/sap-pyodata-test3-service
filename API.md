# API.md — SAP S/4HANA APIs

## Scope

This document covers the SAP-side OData APIs used by the system:

- `API_BUSINESS_PARTNER`
- `API_PRODUCT_SRV`
- `API_SALES_ORDER_SRV`
- `API_PURCHASEORDER_PROCESS_SRV`

The document is based on current official SAP Help Portal / SAP Business Accelerator Hub pages and is intentionally conservative: it only states entity sets, operations, and behaviors that are visible in SAP’s official documentation. For the full field catalog of any service, always confirm against `/$metadata` in the target tenant.

---

## 1. SAP API Architecture Overview

### 1.1 What SAP S/4HANA APIs are

SAP S/4HANA exposes standard business objects as web services so external systems can create, read, update, and delete business data in a controlled way. SAP’s own API pages describe the four APIs in this document as synchronous inbound services for master and transactional objects. citeturn525725search0turn525725search1turn156898search1turn348385search0

### 1.2 OData vs SOAP vs REST in SAP

SAP publishes both OData and SOAP APIs. In the SAP Help Portal, the API catalogs are organized by business area, and the product and sales catalogs explicitly show OData and SOAP options where applicable. For the services covered here, the APIs in use are OData services. citeturn525725search17turn525725search18turn525725search11

### 1.3 How OData works

OData services model SAP business objects as:
- **Entity types**: the object schema.
- **Entity sets**: collections of entities, typically exposed below the service root.
- **Navigation properties**: links to child or related entities.
- **Metadata**: the `/$metadata` document that describes schema and relationships.

SAP’s official pages show standard query options such as `$select`, `$filter`, `$orderby`, `$skip`, `$top`, and `$expand`, and SAP documents batch requests and CSRF handling for write operations. citeturn525725search4turn525725search5turn525725search9turn525725search28turn156898search10

### 1.4 OData V2 vs V4

SAP continues to support both OData V2 and OData V4. SAP explicitly notes that V4 improves processing time and resource consumption, and the Purchase Order V2 API is marked deprecated in SAP S/4HANA 2023 in favor of the V4 successor. citeturn525725search3turn156898search3

### 1.5 How SAP exposes APIs via CDS / released business objects

SAP’s public APIs are published as released business APIs, often aligned with communication scenarios, and consumed through the service root plus `/$metadata`. In practical integration work, the service root is what matters to consumers, while the metadata file is the source of truth for entity names, associations, and supported operations. citeturn525725search24turn348385search1turn156898search10

---

## 2. SAP API Discovery & Ecosystem

### 2.1 SAP Business Accelerator Hub

SAP Business Accelerator Hub is the official catalog for SAP APIs and integration content. SAP’s own help pages state that APIs can be discovered there, tried out in a sandbox, and consumed using generated code snippets. The sandbox uses an API key. citeturn525725search0turn525725search1turn525725search2turn525725search24

### 2.2 Organization model

SAP organizes APIs by business domain and communication scenario. Examples relevant to this system:

- Business Partner / Customer / Supplier: `SAP_COM_0008`
- Product Master: `SAP_COM_0009`
- Sales Order: `SAP_COM_0109`
- Purchase Order: `SAP_COM_0053` citeturn525725search12turn525725search1turn156898search4turn348385search0

### 2.3 Inbound vs outbound

This document covers inbound APIs: the external application calls SAP synchronously over HTTP. SAP also has outbound notifications and event-style integration content in the same business domains, but those are not the APIs used here. citeturn156898search8turn525725search11

### 2.4 Authentication

**Sandbox / API Hub**
- API key authentication is used in SAP Business Accelerator Hub sandbox examples. citeturn525725search24turn525725search0

**Production**
- Production S/4HANA integrations typically use communication users and communication arrangements.
- SAP documents secure inbound communication using OAuth-based and other enterprise authentication patterns depending on the scenario. citeturn525725search7turn525725search24

### 2.5 Common request headers

```http
Accept: application/json
Content-Type: application/json
X-CSRF-Token: Fetch
APIKey: <sandbox-api-key>   # sandbox only, when applicable
```

For write requests, a CSRF token must be fetched and then echoed back in the modifying request. SAP documents this pattern for OData APIs. citeturn525725search28turn525725search0

---

## 3. Detailed Documentation of Each API Used

---

# 3.1 `API_BUSINESS_PARTNER`

## 3.1.1 Overview

**Business purpose**  
Business Partner master data, including customer and supplier-related master data. SAP explicitly describes the API as CRUD-capable for Business Partner, Customer, and Supplier objects. citeturn525725search0turn525725search24

**Business domain**  
Cross-application master data, commonly used in FI/SD/MM master data integration. The API is published under the Business Partner / Customer / Supplier area. citeturn525725search24turn525725search0

## 3.1.2 Technical details

**Service root**
```text
/sap/opu/odata/sap/API_BUSINESS_PARTNER
```

**Metadata**
```text
/sap/opu/odata/sap/API_BUSINESS_PARTNER/$metadata
```

**Verified entity sets / nodes mentioned by SAP**
- `A_BusinessPartner`
- `A_BusinessPartnerAddress`
- `A_BusinessPartnerBank`
- `A_BusinessPartnerContact`
- `A_BusinessPartnerRating`
- `A_BusinessPartnerRole`
- `A_BPDataController`
- `A_BuPaIndustry`
- `A_CustomerCompany`
- `A_CustomerSalesArea`
- `A_SupplierCompany` citeturn525725search0turn525725search12turn525725search28

**Key fields**
- `BusinessPartner` (primary identifier in examples) citeturn525725search4turn525725search16

**Common navigation properties**
- `to_BusinessPartnerAddress`
- `to_BusinessPartnerBank`
- `to_BusinessPartnerContact`
- `to_BusinessPartnerRole`
- `to_BusinessPartnerRating`
- `to_BuPaIndustry` citeturn525725search0turn525725search4

## 3.1.3 Entity schema deep dive

SAP’s public documentation shows the following fields in example payloads and descriptions:

| Field | Notes |
|---|---|
| `BusinessPartnerGrouping` | Used in create examples |
| `BusinessPartnerCategory` | Used in create examples |
| `OrganizationBPName1` | Used in create examples |
| `BusinessPartner` | Main identifier |
| `BusinessPartnerRole` | Role assignment node |
| `BusinessPartnerAddress` | Address child entity |
| `BusinessPartnerBank` | Bank child entity |
| `BusinessPartnerContact` | Contact child entity |

SAP supports deep payloads for create and update. For exact data types and the complete field list, inspect `/$metadata` in the target tenant. citeturn525725search12turn525725search0turn525725search4turn525725search28

## 3.1.4 Supported operations

- `GET`
- `POST`
- `PATCH`
- `DELETE`
- `$batch` support for grouped operations citeturn525725search4turn525725search12turn525725search28

SAP documents read, create-with-deep-payload, update, and batch scenarios for this API. citeturn525725search4turn525725search12turn525725search28

## 3.1.5 Query capabilities

Supported OData options used in SAP examples:
- `$select`
- `$filter`
- `$expand`
- `$orderby`
- `$top`
- `$skip` citeturn525725search4turn525725search28

## 3.1.6 Example requests

### Read a business partner
```http
GET /sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner('1000001')?$format=json HTTP/1.1
Accept: application/json
```

### Create a business partner
```http
POST /sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner HTTP/1.1
Accept: application/json
Content-Type: application/json
X-CSRF-Token: Fetch

{
  "BusinessPartnerGrouping": "0001",
  "BusinessPartnerCategory": "2",
  "OrganizationBPName1": "Acme Trading LLC"
}
```

### Deep update example pattern
```http
PATCH /sap/opu/odata/sap/API_BUSINESS_PARTNER/A_BusinessPartner('1000001') HTTP/1.1
Accept: application/json
Content-Type: application/json
If-Match: *
X-CSRF-Token: <token>
```

---

# 3.2 `API_PRODUCT_SRV`

## 3.2.1 Overview

**Business purpose**  
Product master data create/read/update/delete service. SAP’s Product Master API page explicitly says it is a synchronous inbound service for CRUD operations on master data. citeturn525725search1turn525725search13

**Business domain**  
Material / product master data used across procurement, sales, logistics, valuation, and text maintenance. citeturn525725search1turn525725search5turn525725search9

## 3.2.2 Technical details

**Service root**
```text
/sap/opu/odata/sap/API_PRODUCT_SRV
```

**Metadata**
```text
/sap/opu/odata/sap/API_PRODUCT_SRV/$metadata
```

**Verified entity sets / nodes mentioned by SAP**
- `A_Product`
- `A_ProductDescription`
- `A_ProductPlant`
- `A_ProductBasicText`
- `A_ProductInspectionText`
- `A_ProductProcurement`
- `A_ProductPurchaseText`
- `A_ProductQualityMgmt`
- `A_ProductSales`
- `A_ProductSalesTax`
- `A_ProductStorageLocation`
- `A_ProductValuation`
- `A_ProductSalesDelivery`
- `A_ProductSalesDeliveryText`
- `A_ProductSalesText` citeturn525725search5turn525725search9turn525725search13

**Key fields**
- `Product` (primary key in SAP examples) citeturn525725search5turn525725search13

**Common navigation/child areas**
- plant data
- sales data
- valuation data
- descriptions/texts
- procurement data
- storage-location data citeturn525725search5turn525725search9turn525725search13

## 3.2.3 Entity schema deep dive

SAP examples visibly include these fields:

| Field | Notes |
|---|---|
| `Product` | Main identifier |
| `ProductType` | Seen in sample response payloads |
| `CrossPlantStatus` | Seen in sample response payloads |
| `Plant` | Appears in plant-level child entities |
| `ValuationArea` | Appears in valuation-related content |
| `ProductSalesOrg` | Appears in sales data pages |
| `ProductDistributionChnl` | Appears in sales-related pages |

SAP documents deep payloads for create and update. The complete field list and exact data types must be read from `/$metadata`. citeturn525725search5turn525725search9turn525725search13

## 3.2.4 Supported operations

- `GET`
- `POST`
- `PATCH`
- `DELETE`
- `$batch` support citeturn525725search1turn525725search13turn525725search28

## 3.2.5 Query capabilities

Supported OData query options in SAP product pages include:
- `$select`
- `$filter`
- `$expand`
- `$orderby`
- `$top`
- `$skip`
- `$count` in collection scenarios citeturn525725search5turn525725search13

## 3.2.6 Example requests

### Read product master data
```http
GET /sap/opu/odata/sap/API_PRODUCT_SRV/A_Product(Product='DEMOPRODUCT001')?$format=json HTTP/1.1
Accept: application/json
```

### Create or update product master data
```http
POST /sap/opu/odata/sap/API_PRODUCT_SRV/A_Product HTTP/1.1
Accept: application/json
Content-Type: application/json
X-CSRF-Token: Fetch

{
  "Product": "DEMOPRODUCT001",
  "ProductType": "FERT",
  "CrossPlantStatus": "1"
}
```

---

# 3.3 `API_SALES_ORDER_SRV`

## 3.3.1 Overview

**Business purpose**  
Create, read, update, and delete sales orders in an external system. SAP explicitly names this service “Sales Order (A2X, OData V2)” and states the technical name is `API_SALES_ORDER_SRV`. citeturn525725search2turn156898search1turn156898search10

**Business domain**  
Sales and Distribution / order-to-cash. SAP’s sales API catalog groups this service under APIs for Sales. citeturn525725search18turn156898search4

## 3.3.2 Technical details

**Service root**
```text
/sap/opu/odata/sap/API_SALES_ORDER_SRV
```

**Metadata**
```text
/sap/opu/odata/sap/API_SALES_ORDER_SRV/$metadata
```

**Verified entity sets / nodes mentioned by SAP**
- `A_SalesOrder`
- `A_SalesOrderItem`
- item pricing-related nodes
- partner address variants for sales order creation
- other child structures exposed in the service pages citeturn156898search10turn156898search13turn156898search14turn156898search19turn156898search23

**Key fields**
- Sales order number is used as the main identifier in SAP examples.
- Item-level entities are addressed by the sales order plus item key in child requests. citeturn156898search0turn156898search19turn156898search22

**Common navigation properties**
- item collections from header to items
- item-level dependent structures such as pricing elements and partner/address-related child data citeturn156898search0turn156898search13turn156898search23

## 3.3.3 Entity schema deep dive

SAP’s examples show the following business data areas:

| Area | Notes |
|---|---|
| Header data | `A_SalesOrder` |
| Item data | `A_SalesOrderItem` |
| Pricing | item pricing elements |
| Partner addresses | document-specific address handling |
| Reference-based creation | creation with contract/reference documents |

The public SAP pages for this service focus on business scenarios and request examples. For field types and the complete schema, use `/$metadata`. citeturn156898search7turn156898search10turn156898search13turn156898search14turn156898search23

## 3.3.4 Supported operations

SAP documents:
- `GET`
- `POST`
- `PATCH`
- `DELETE`
- item-level operations
- create with document-specific address
- create with reference
- batch-capable OData patterns where supported citeturn156898search0turn156898search7turn156898search13turn156898search19turn156898search21

## 3.3.5 Query capabilities

Standard OData query options are supported in the service ecosystem:
- `$select`
- `$filter`
- `$expand`
- `$orderby`
- `$top`
- `$skip` citeturn156898search10turn156898search4

## 3.3.6 Example requests

### Create a sales order
```http
POST /sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder HTTP/1.1
Accept: application/json
Content-Type: application/json
X-CSRF-Token: Fetch

{
  "SalesOrderType": "OR",
  "SalesOrganization": "1000",
  "DistributionChannel": "10",
  "OrganizationDivision": "00"
}
```

### Create an item
```http
POST /sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrderItem HTTP/1.1
Accept: application/json
Content-Type: application/json
X-CSRF-Token: Fetch

{
  "SalesOrder": "5000000001",
  "SalesOrderItem": "000010",
  "Material": "TG-17",
  "RequestedQuantity": "1"
}
```

---

# 3.4 `API_PURCHASEORDER_PROCESS_SRV`

## 3.4.1 Overview

**Business purpose**  
Purchase order processing in S/4HANA. SAP identifies the technical API name as `API_PURCHASEORDER_PROCESS_SRV`. The SAP Help Portal states that the OData V2 Purchase Order API is deprecated with SAP S/4HANA 2023 and should be replaced by the V4 API for new work. citeturn348385search0turn156898search2

**Business domain**  
Sourcing and Procurement / Materials Management. SAP lists this API under APIs in Sourcing and Procurement. citeturn525725search11turn348385search1

## 3.4.2 Technical details

**Service root**
```text
/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV
```

**Metadata**
```text
/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/$metadata
```

**Verified entity sets / nodes mentioned by SAP**
- `A_PurchaseOrder`
- `A_PurchaseOrderItem`
- `A_PurchaseOrderScheduleLine`
- `A_PurchaseOrderItemNote`
- `A_PurchaseOrderHeaderText` or header text-related node names may vary by released service content; always verify in `/$metadata` for your tenant
- related procurement lookup entities such as purchasing organization and group are documented in the broader procurement catalog citeturn348385search4turn156898search5turn348385search11turn348385search23

**Key fields**
- Purchase order number is used as the main identifier in SAP examples. citeturn348385search4turn156898search5

**Common navigation properties**
- header to items
- items to schedule lines
- items to item notes
- item-specific substructures for subcontracting / account assignment in the broader procurement model citeturn156898search5turn348385search8turn348385search13turn348385search18turn348385search21

## 3.4.3 Entity schema deep dive

SAP’s official pages explicitly show these entity groups:

| Area | Notes |
|---|---|
| Header | `A_PurchaseOrder` |
| Items | `A_PurchaseOrderItem` |
| Schedule lines | `A_PurchaseOrderScheduleLine` |
| Item notes | `A_PurchaseOrderItemNote` |
| Related procurement details | exposed in procurement catalog pages |

SAP marks the V2 API as deprecated and points to the V4 purchase order API for forward-looking implementations. Use `/$metadata` to verify the exact child entities and types in the tenant in use. citeturn348385search0turn156898search3turn156898search5turn156898search8

## 3.4.4 Supported operations

- `GET`
- `POST`
- `PATCH`
- `DELETE`
- child-entity operations
- batch patterns where supported by the OData service citeturn348385search4turn156898search5turn348385search0

## 3.4.5 Query capabilities

Standard OData query options are used throughout SAP procurement examples:
- `$select`
- `$filter`
- `$expand`
- `$orderby`
- `$top`
- `$skip` citeturn348385search4turn156898search5turn348385search1

## 3.4.6 Example requests

### Read a purchase order
```http
GET /sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder('4500100268')?$format=json HTTP/1.1
Accept: application/json
```

### Read an item collection
```http
GET /sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder('4500100268')/to_PurchaseOrderItem?$format=json HTTP/1.1
Accept: application/json
```

### Create or update pattern
```http
PATCH /sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder('4500100268') HTTP/1.1
Accept: application/json
Content-Type: application/json
If-Match: *
X-CSRF-Token: <token>
```

---

## 4. OData Deep Dive (SAP-specific)

### 4.1 Query system

SAP OData services support the classic query system:
- `$filter` for server-side filtering
- `$select` to reduce payload
- `$expand` to pull related entities
- `$orderby` for deterministic sorting
- `$top` / `$skip` for pagination citeturn525725search4turn525725search5turn156898search10

### 4.2 Metadata structure

`/$metadata` is the authoritative schema document. Use it to confirm:
- entity set names
- key properties
- property types
- navigation properties
- multiplicities
- supported actions / functions citeturn156898search10turn525725search4turn525725search5

### 4.3 Navigation properties and associations

SAP’s service pages commonly expose child collections through navigation properties. In integration code, this is how you read a header and then move to items, texts, partner addresses, or schedule lines without separate object lookups. citeturn156898search13turn156898search0turn348385search4turn525725search0

### 4.4 Common SAP quirks

- V2 and V4 naming patterns are not interchangeable.
- Some APIs are deprecated and replaced by a newer version.
- Deep payload support exists in selected APIs but not universally.
- The same business object may have multiple services across cloud/on-premise scopes.
- Some public help pages show service examples under `/sap/opu/odata/SAP/...` with uppercase `SAP`, while runtime systems often accept the standard lowercase form in documentation examples; follow the tenant’s actual service URL. citeturn348385search0turn156898search3turn156898search10turn525725search12

---

## 5. Authentication & Security

### 5.1 API key usage in SAP API Hub sandbox

SAP’s sandbox examples use an API key and generated code snippets can include it. This is for SAP Business Accelerator Hub testing only. citeturn525725search24turn525725search0

### 5.2 OAuth and production access

For production S/4HANA, use the communication arrangement / communication user pattern mandated by SAP for inbound integration. The exact mechanism depends on the tenant and API, but SAP’s secure communication guidance places authentication and authorization under the S/4HANA communication framework rather than public API Hub keys. citeturn525725search7turn525725search24

### 5.3 CSRF protection

For state-changing requests in OData, fetch a CSRF token before POST / PATCH / DELETE, then send it back in the modifying request. SAP explicitly documents this pattern for OData consumption. citeturn525725search28turn525725search0

### 5.4 Recommended security posture

- Use least-privilege communication users.
- Restrict service activation to the APIs actually used.
- Avoid embedding sandbox API keys in production code.
- Treat metadata and example payloads as discoverable but not sufficient for authorization design. citeturn525725search7turn525725search24

---

## 6. Error Handling

### 6.1 SAP OData error shape

SAP OData errors are returned as structured HTTP errors with a service-specific payload. In integration practice, assume:
- HTTP status code conveys transport/result class.
- Response body contains the OData error details.
- The message text is often the most useful troubleshooting clue.

### 6.2 Common error patterns

- Missing or invalid CSRF token
- Authorization failure
- Invalid key predicate
- Validation failure on required business fields
- Version mismatch between V2 and V4 service contracts
- Deep payload rejected because the target node is not released for write in that API version citeturn525725search28turn348385search0turn156898search3

### 6.3 Troubleshooting pattern

1. Verify the exact service root.
2. Verify `$metadata`.
3. Confirm authentication and CSRF behavior.
4. Reduce the payload to a minimal valid request.
5. Add child entities only after the header works.
6. Test the same request with `?$format=json` and a minimal `$select`. citeturn525725search4turn525725search5turn156898search10

---

## 7. Performance & Limits

### 7.1 Pagination strategy

For collection reads, always page through results with `$top` and `$skip` rather than retrieving large uncontrolled datasets. This reduces payload size and avoids timeouts. SAP examples consistently use server-side query options for filtered and paged reads. citeturn525725search4turn525725search5

### 7.2 Payload minimization

Prefer:
- `$select` for narrow projections
- `$expand` only when needed
- header-only reads before drilling into child entities
- write requests that include only the required fields citeturn525725search4turn525725search5turn156898search10

### 7.3 Batch usage

Use `$batch` when several dependent OData operations must be sent together, especially when the target system and service support atomic grouping. SAP documents batch handling for OData APIs. citeturn525725search28turn525725search0

### 7.4 Rate limiting

SAP’s public pages for the services covered here do not present a universal numeric rate limit in the referenced pages. For production architecture, treat throttling as tenant-specific and confirm with the target SAP landscape team. This is an operational inference from SAP’s published service documentation, not a documented universal limit. citeturn525725search0turn525725search1turn525725search2turn348385search0

---

## 8. Known SAP Quirks / Gotchas

### 8.1 Metadata-first discipline

Do not assume a field is writable or even present just because it exists in one API version or another. SAP releases can differ between cloud and on-premise, and between V2 and V4. The `/$metadata` document is the contract. citeturn525725search1turn156898search3turn156898search10

### 8.2 V2 vs V4 response shape differences

The Purchase Order V2 API is deprecated; the V4 API has a different service contract and should not be treated as a drop-in wire-compatible replacement. citeturn348385search0turn156898search3

### 8.3 Field naming inconsistencies

SAP APIs may expose similar business concepts under slightly different names depending on object, version, or service scope. For example, sales-order and purchase-order child structures are not normalized across services. Always map by actual service metadata, not by naming intuition. citeturn156898search10turn156898search5turn525725search5

### 8.4 Deep payload support is selective

Business Partner and Product explicitly document deep payload scenarios. Sales Order also exposes rich child structures. Purchase Order V2/V4 differ materially. Do not assume deep insert works everywhere. citeturn525725search12turn525725search9turn156898search13turn156898search3

---

## 9. Mapping to Real Business Processes

| API | Business process | Typical business meaning |
|---|---|---|
| `API_BUSINESS_PARTNER` | Customer / vendor / BP master | Golden record for sold-to, ship-to, payer, supplier, etc. |
| `API_PRODUCT_SRV` | Material / product master | Core item master for sales, procurement, valuation |
| `API_SALES_ORDER_SRV` | Order-to-cash | Customer order capture and fulfillment |
| `API_PURCHASEORDER_PROCESS_SRV` | Procure-to-pay | Procurement execution and supplier ordering |

SAP’s official catalogs group these APIs exactly in the master-data, sales, and sourcing/procurement domains. citeturn525725search24turn525725search18turn525725search11

---

## 10. Best Practices

### 10.1 Efficient querying

- Use `$select` to limit fields.
- Use `$filter` to keep reads narrow.
- Avoid fetching child entities unless required.
- Read headers first, then expand or drill into children only when needed. citeturn525725search4turn525725search5turn156898search10

### 10.2 Minimizing payload size

- Send only writable fields in create/update requests.
- Prefer deep payloads only when SAP explicitly documents them.
- Keep JSON payloads aligned to the service metadata. citeturn525725search12turn525725search9turn156898search13

### 10.3 Handling pagination

- Always implement cursorless pagination with `$top` / `$skip`.
- Preserve sort order with `$orderby` before paging.
- Do not assume stable order without explicit sorting. citeturn525725search4turn525725search5

### 10.4 Error resilience

- Retry only idempotent reads automatically.
- For writes, verify whether the request already succeeded before retrying.
- Surface SAP error text in integration logs.
- Keep the original request payload with the error record for diagnosis. citeturn525725search28turn525725search0

---

## 11. Reference requests

### 11.1 Generic OData read

```http
GET /sap/opu/odata/sap/<SERVICE_NAME>/<ENTITY_SET>?$select=<fields>&$filter=<expr>&$top=50&$skip=0&$format=json HTTP/1.1
Accept: application/json
```

### 11.2 Generic write with CSRF

```http
POST /sap/opu/odata/sap/<SERVICE_NAME>/<ENTITY_SET> HTTP/1.1
Accept: application/json
Content-Type: application/json
X-CSRF-Token: Fetch
```

---

## 12. Official SAP References

### SAP Help Portal / SAP Business Accelerator Hub
- Business Partner (A2X) – OData API: https://help.sap.com/docs/SAP_S4HANA_CLOUD/3c916ef10fc240c9afc594b346ffaf77/85043858ea0f9244e10000000a4450e5.html
- Read Business Partner Data: https://help.sap.com/docs/SAP_S4HANA_CLOUD/3c916ef10fc240c9afc594b346ffaf77/8d11d39c4efd42c0ad1392867df16f32.html
- Create Business Partner Data with Deep Payload: https://help.sap.com/docs/SAP_S4HANA_CLOUD/3c916ef10fc240c9afc594b346ffaf77/496d837766f74369a96bc0594ad6a4dc.html
- Update Business Partner Data: https://help.sap.com/docs/SAP_S4HANA_CLOUD/3c916ef10fc240c9afc594b346ffaf77/81c9afd408d24612a580ad0c3f77c8a5.html
- APIs for Business Partners, Customers, and Suppliers: https://help.sap.com/docs/SAP_S4HANA_CLOUD/3c916ef10fc240c9afc594b346ffaf77/a9ee5e5297604ec29eb1a7ec844d96ad.html
- APIs for Product Master: https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/18fe3fab96864826bfa0be0de4f65b85/a8661dda13ef407abc16902e4da68361.html
- Read Product Master Data: https://help.sap.com/docs/SAP_S4HANA_CLOUD/3c916ef10fc240c9afc594b346ffaf77/2bd6b919cc794fc6bebb5a2167b3921d4.html
- Update Product Master Data: https://help.sap.com/docs/SAP_S4HANA_CLOUD/3c916ef10fc240c9afc594b346ffaf77/d2d45480188e4752a778bd173b54384a.html
- Sales Order (A2X, OData V2): https://help.sap.com/docs/SAP_S4HANA_CLOUD/03c04db2a7434731b7fe21dca77440da/00d244581efca007e10000000a441470.html
- APIs for Sales: https://help.sap.com/docs/SAP_S4HANA_CLOUD/03c04db2a7434731b7fe21dca77440da/82b46ca209f94853b3cf7e3419817ea7.html
- Create Sales Order Item: https://help.sap.com/docs/SAP_S4HANA_CLOUD/03c04db2a7434731b7fe21dca77440da/5e78feff2ce74328b7305146f61b88da.html
- Update Sales Order Item: https://help.sap.com/docs/SAP_S4HANA_CLOUD/03c04db2a7434731b7fe21dca77440da/d1f850761f034829b6330e476433dc66.html
- Create Sales Order with Document-Specific Address: https://help.sap.com/docs/SAP_S4HANA_CLOUD/03c04db2a7434731b7fe21dca77440da/c64a1b01db3347efb6b23e7ec73347ee.html
- Create Sales Orders with Reference: https://help.sap.com/docs/SAP_S4HANA_CLOUD/03c04db2a7434731b7fe21dca77440da/03373661272d43b0b43538f171ae6aba.html
- OData V2 API: Purchase Order: https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/f296651f454c4284ade361292c633d69/3596c812af884e7f9ddbd90ef9a8c20c.html
- Purchase Order (OData V4): https://help.sap.com/docs/SAP_S4HANA_CLOUD/bb9f1469daf04bd894ab2167f8132a1a/c89eec80ec2043d980cb7b8c89e0a00a.html
- APIs in Sourcing and Procurement: https://help.sap.com/docs/SAP_S4HANA_CLOUD/bb9f1469daf04bd894ab2167f8132a1a/807238156726425dbd7f7ff8afc24da1.html
- Read Purchase Order with Schedule Line and Subcontracting Component: https://help.sap.com/docs/SAP_S4HANA_CLOUD/bb9f1469daf04bd894ab2167f8132a1a/4bf51821d3434ce7975de25c6fd8643b.html
- SAP Business Accelerator Hub sandbox documentation: https://help.sap.com/docs/business-accelerator-hub/sap-business-accelerator-hub/trying-out-apis-in-sandbox-environment
- SAP Business Accelerator Hub code snippets: https://help.sap.com/docs/business-accelerator-hub/sap-business-accelerator-hub/consuming-api-using-code-snippet
- API details on SAP Business Accelerator Hub: https://help.sap.com/docs/business-accelerator-hub/sap-business-accelerator-hub/api-details?version=Cloud
- CSRF token handling: https://help.sap.com/docs/SAP_S4HANA_CLOUD/0f69f8fb28ac4bf48d2b57b9637e81fa/b886f94e821147eab21a90f5288a20e3.html
- Batch requests: https://help.sap.com/docs/SAP_S4HANA_CLOUD/3c916ef10fc240c9afc594b346ffaf77/43e229cb62ea40ab9979953d188daf20.html
