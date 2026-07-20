# Usage

## Python API

```python
from gramps_mcp.auth import get_client

client = get_client()
try:
    result = client.get_people(page=1, pagesize=25)
    print(result.status_code)
finally:
    client.close()
```

`get_client()` reads the AgentConfig projection. Pass explicit values only in isolated
tests; production code should not embed an endpoint or credential.

## Condensed MCP

Each domain tool accepts an action and a JSON string:

```json
{
  "tool": "gramps_people",
  "arguments": {
    "action": "get_person",
    "params_json": "{\"handle\":\"<record-handle>\"}"
  }
}
```

Use a narrow search to resolve a handle, then read referenced families, events, sources,
and citations explicitly. A display identifier is not a substitute for the stable
handle.

## Safe mutations

Read the current object and state the intended result before any write. Obtain explicit
scope for merges, imports, deletes, transaction undo, tree repair or migration, owner or
user changes, password or token operations, and bulk media or export actions. Execute the
smallest approved operation and read the affected record back.

Avoid printing whole records. Report stable identifiers, status, counts, and the minimum
evidence needed to answer the question.

## Source synchronization

Do not call a provider graph-write tool; none is registered. Request the central GraphOS
source-sync capability only after its signed bundle, exact schema pins, and genealogy
data policy have been approved.
