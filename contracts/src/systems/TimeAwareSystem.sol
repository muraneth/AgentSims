// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { System, IWorld } from "solecs/System.sol";
import { getAddressById, addressToEntity } from "solecs/utils.sol";
import { TimeAwareComponent, ID as TimeAwareComponentID } from "components/TimeAwareComponent.sol";
import { SingletonID } from "solecs/SingletonID.sol";

uint256 constant ID = uint256(keccak256("system.TimeAware"));

contract TimeAwareSystem is System {
  constructor(IWorld _world, address _components) System(_world, _components) {}

  function execute(bytes memory args) public returns (bytes memory) {
    uint256 timestamp = abi.decode(args, (uint256));
    return executeTyped(timestamp);
  }

  function executeTyped(uint256 timestamp) public returns (bytes memory) {
    TimeAwareComponent timeAware = TimeAwareComponent(getAddressById(components, TimeAwareComponentID));
    timeAware.set(SingletonID, timestamp);

    return new bytes(0);
  }
}
