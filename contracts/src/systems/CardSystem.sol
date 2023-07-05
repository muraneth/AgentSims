// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { System, IWorld } from "solecs/System.sol";
import { getAddressById, addressToEntity } from "solecs/utils.sol";
import { CardComponent, ID as CardComponentID, Card, SUIT, RANK } from "components/CardComponent.sol";
import { LibMap } from "libraries/LibMap.sol";

uint256 constant ID = uint256(keccak256("system.Card"));

struct InputParams {
    SUIT suit;
    RANK rank;
    uint256 targetId;
}

contract CardSystem is System {

  constructor(IWorld _world, address _components) System(_world, _components) {}

  function execute(bytes memory args) public returns (bytes memory) {
    return executeTyped(abi.decode(args, (InputParams)));
  }

  function executeTyped(InputParams memory inputParams) public returns (bytes memory) {
    uint256 entityId = addressToEntity(msg.sender);

    Card memory card = Card(inputParams.suit, inputParams.rank);
    CardComponent cardComponent = CardComponent(getAddressById(components, CardComponentID));
    cardComponent.set(inputParams.targetId, card);
    return new bytes(0);
  }
}
