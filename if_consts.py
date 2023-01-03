# This does not include transfers
SUPPORTED_ACTIONS = ['accept', 'cite', 'consume', 'modify', 'produce', 'use', 'work']
IN_PR_ACTIONS = ['accept', 'cite', 'consume', 'use', 'work']
OUT_PR_ACTIONS = ['modify', 'produce']
assert set(IN_PR_ACTIONS + OUT_PR_ACTIONS) == set(SUPPORTED_ACTIONS)


MAX_DEPTH = 100000000
AGENT_FRAG = """
    fragment agent on Agent {
        id
        name
    }
"""
LOCATION_FRAG = """
    fragment location on SpatialThing {
        id
        alt
        lat
        long
        mappableAddress
        name
        note
    }
"""
QUANTITY_FRAG = """
    fragment quantity on Measure {
      hasNumericalValue
      hasUnit {
        id
        label
        symbol
      }

    }
"""

RESOURCE_FRAG = """
    fragment resource on EconomicResource {
            id
            name
            onhandQuantity {
                ...quantity
            }
            accountingQuantity {
                ...quantity
            }
            primaryAccountable {
                ...agent
            }
            custodian {
                ...agent
            }
          }
"""
