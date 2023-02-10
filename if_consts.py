# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2022-2023 Dyne.org foundation <foundation@dyne.org>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# This does not include transfers
SUPPORTED_ACTIONS = ['accept', 'cite', 'consume', 'modify', 'produce', 'use', 'work', 'deliverService']
IN_PR_ACTIONS = ['accept', 'cite', 'consume', 'use', 'work']
OUT_PR_ACTIONS = ['modify', 'produce']
IN_OUT_PR_ACTIONS = ['deliverService']
assert set(IN_PR_ACTIONS + OUT_PR_ACTIONS + IN_OUT_PR_ACTIONS) == set(SUPPORTED_ACTIONS)


MAX_DEPTH = 100000000
AGENT_FRAG = """
    fragment agent on Agent {
        id
        name
        type: __typename
        note
        primaryLocation {
            ...location
        }
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
            trackingIdentifier
            type: __typename
            metadata
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
            currentLocation {
                ...location
            }
          }
"""
UNIT_FRAG = """
    fragment unit on Unit {
        id
        label
        symbol
}
"""
RESSPEC_FRAG = """
    fragment resourcespecification on ResourceSpecification {
        defaultUnitOfEffort {
            ...unit
        }
        defaultUnitOfResource {
            ...unit
        }
        id
        name
        note
        resourceClassifiedAs
    }
"""

ACTION_FRAG = """
    fragment action on Action {
        id
        inputOutput
        label
        onhandEffect
        pairsWith
        resourceEffect
    }
"""
PROCESSSPEC_FRAG = """
    fragment processspecification on ProcessSpecification {
        id
        name
        note
    }
"""
PROCESS_FRAG = """
    fragment process on Process {
        type: __typename
        basedOn {
            ...processspecification
        }
        classifiedAs
        deletable
        finished
        hasBeginning
        hasEnd
        id
        name
        nestedIn {
            id
        }
        # Scenario The process with its inputs and outputs is part of the scenario.

        note
        plannedWithin {
            id
        }
        # Plan: The process with its inputs and outputs is part of the plan.
    }
"""
PROCESSGRP_FRAG = """
    fragment processgroup on ProcessGroup {
        groupedIn {
            id
            name
            note
        }
        id
        name
        type: __typename
        note
        groups(first:100) {
            edges {
                cursor
                node {
                    __typename
                    ...on Process {
                        ...process
                    }
                    ...on ProcessGroup {
                        id
                        name
                        note
                    }
                }
            }
        }
    }
"""        

EVENT_FRAG = """
    fragment event on EconomicEvent {
        type : __typename
        action {
            ...action
        }
        agreedIn
        # String Reference to an agreement between agents which specifies the rules or policies or calculations which govern this economic event.

        atLocation {
            ...location
        }

        effortQuantity {
            ...quantity
        }
        hasBeginning
        hasEnd
        hasPointInTime
        id
        inputOf {
            ...process
        }
        outputOf {
            ...process
        }
        note
        provider {
            ...agent
        }
        receiver {
            ...agent
        }

        realizationOf {
            id
        }
        # Agreement This economic event occurs as part of this agreement.

        resourceClassifiedAs
        resourceConformsTo {
            ...resourcespecification
        }
        resourceInventoriedAs {
            ...resource
        }

        resourceQuantity {
            ...quantity
        }
        toLocation {
            ...location
        }
        toResourceInventoriedAs {
            ...resource
        }
        triggeredBy {
            id
        }
    }
"""
# Potentially recursive fragment

PROPINT_FRAG = """
    fragment proposedintent on ProposedIntent {
        id 
        publishedIn {
            id
            name
        }
    
        publishes {
            id
            name
        }
        reciprocal
    }
"""
    
INTENT_FRAG = """
    fragment intent on Intent {
        name
        note
        id
        action {
            ...action
        }
        agreedIn
        atLocation {
            ...location
        }
        availableQuantity {
            ...quantity
        }
        
        # deletable
        due
        effortQuantity {
            ...quantity
        }
        finished
        hasBeginning
        hasEnd
        hasPointInTime

        inputOf {
            ...process
        }
        outputOf {
            ...process
        }
        
        provider {
            ...agent
        }
        receiver {
            ...agent
        }
        
        publishedIn {
            ...proposedintent
        }
        resourceClassifiedAs
        
        resourceConformsTo {
            ...resourcespecification
        }

        resourceInventoriedAs {
            ...resource
        }
        resourceQuantity {
            ...quantity
        }
    }
"""

PROPOSAL_FRAG = """
    fragment proposal on Proposal {
        created
        eligibleLocation {
            ...location
        }
        hasBeginning
        hasEnd
        id
        name
        note
        primaryIntents {
            ...intent
        }
        publishes {
            ...proposedintent
        }
        reciprocalIntents {
            ...intent
        }
        status
        unitBased
    }

"""