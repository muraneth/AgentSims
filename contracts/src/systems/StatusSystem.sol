// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { System, IWorld } from "solecs/System.sol";
import { getAddressById, addressToEntity } from "solecs/utils.sol";
import { StatusComponent, ID as StatusComponentID } from "components/StatusComponent.sol";
import { LibMap } from "libraries/LibMap.sol";

uint256 constant ID = uint256(keccak256("system.Status"));

// struct StatusDetail {
//     uint256 entityId;
//     string detail;
// }

contract StatusSystem is System {

  constructor(IWorld _world, address _components) System(_world, _components) {}

  function execute(bytes memory args) public returns (bytes memory) {
    return executeTyped(abi.decode(args, (string)));
  }

  function executeTyped(string memory status) public returns (bytes memory) {
    uint256 entityId = addressToEntity(msg.sender);

    // Status memory prompt = Status(promptdetail.detail, promptdetail.entityId);
    StatusComponent(getAddressById(components, StatusComponentID)).set(entityId, status);
    return new bytes(0);
  }
}
