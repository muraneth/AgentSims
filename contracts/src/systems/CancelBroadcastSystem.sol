// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { System, IWorld } from "solecs/System.sol";
import { getAddressById, addressToEntity } from "solecs/utils.sol";
import { BroadcastComponent, ID as BroadcastComponentID } from "components/BroadcastComponent.sol";
import { LibMap } from "libraries/LibMap.sol";
import { SingletonID } from "solecs/SingletonID.sol";

uint256 constant ID = uint256(keccak256("system.CancelBroadcast"));

// struct CancelBroadcastDetail {
//     uint256 entityId;
//     string detail;
// }

contract CancelBroadcastSystem is System {

  constructor(IWorld _world, address _components) System(_world, _components) {}

  function execute(bytes memory args) public returns (bytes memory) {
    return executeTyped(abi.decode(args, (string)));
  }

  function executeTyped(string memory broadcast) public returns (bytes memory) {
    // uint256 entityId = addressToEntity(msg.sender);

    // Broadcast memory chat = Broadcast(chatdetail.detail, chatdetail.entityId);
    BroadcastComponent broadcastComponent = BroadcastComponent(getAddressById(components, BroadcastComponentID));
    broadcastComponent.remove(SingletonID);
    return new bytes(0);
  }
}
