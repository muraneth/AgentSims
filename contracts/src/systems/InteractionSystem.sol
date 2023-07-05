// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { System, IWorld } from "solecs/System.sol";
import { getAddressById, addressToEntity } from "solecs/utils.sol";
import { StatusComponent, ID as StatusComponentID } from "components/StatusComponent.sol";
import { PositionComponent, ID as PositionComponentID, Coord } from "components/PositionComponent.sol";
import { InteractiveComponent, ID as InteractiveComponentID } from "components/InteractiveComponent.sol";
import { LibMap } from "libraries/LibMap.sol";

uint256 constant ID = uint256(keccak256("system.Interaction"));

struct Interaction {
    uint256 targetId;
    string interaction;
}

contract InteractionSystem is System {
//   uint256 internal entropyNonce = 1;

  constructor(IWorld _world, address _components) System(_world, _components) {}

  function execute(bytes memory args) public returns (bytes memory) {
    return executeTyped(abi.decode(args, (Interaction)));
  }

  function executeTyped(Interaction memory interaction) public returns (bytes memory) {
    uint256 entityId = addressToEntity(msg.sender);

    // require distance between target & entity <= InteractiveComponent.interaction_range
    InteractiveComponent interactiveComponent = InteractiveComponent(getAddressById(components, InteractiveComponentID));
    require(interactiveComponent.has(interaction.targetId), "Target cannot interact");
    // PositionComponent positionComponent = PositionComponent(getAddressById(components, PositionComponentID));
    // Coord entityPosition = positionComponent.getValue(entityId);
    // Coord targetPosition = positionComponent.getValue(interaction.targetId);
    // require(LibMap.distance(entityPosition, targetPosition) <= interactive, "can only move to adjacent spaces");

    // Status memory status = Status(interaction.interaction, uint64(block.timestamp));
    StatusComponent(getAddressById(components, StatusComponentID)).set(entityId, interaction.interaction);

    return new bytes(0);
  }
}
