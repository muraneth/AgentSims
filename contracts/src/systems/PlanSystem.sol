// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { System, IWorld } from "solecs/System.sol";
import { getAddressById, addressToEntity } from "solecs/utils.sol";
import { PlanComponent, ID as PlanComponentID } from "components/PlanComponent.sol";
import { LibMap } from "libraries/LibMap.sol";

uint256 constant ID = uint256(keccak256("system.Plan"));

// struct PlanDetail {
//     uint256 entityId;
//     string detail;
// }

contract PlanSystem is System {

  constructor(IWorld _world, address _components) System(_world, _components) {}

  function execute(bytes memory args) public returns (bytes memory) {
    return executeTyped(abi.decode(args, (string)));
  }

  function executeTyped(string memory plan) public returns (bytes memory) {
    uint256 entityId = addressToEntity(msg.sender);

    // Plan memory chat = Plan(chatdetail.detail, chatdetail.entityId);
    PlanComponent planComponent = PlanComponent(getAddressById(components, PlanComponentID));
    planComponent.set(entityId, plan);
    return new bytes(0);
  }
}
