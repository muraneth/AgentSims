// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { System, IWorld } from "solecs/System.sol";
import { getAddressById, addressToEntity } from "solecs/utils.sol";
import { CoinComponent, ID as CoinComponentID } from "components/CoinComponent.sol";

uint256 constant ID = uint256(keccak256("system.CostCoin"));

contract CostCoinSystem is System {
  constructor(IWorld _world, address _components) System(_world, _components) {}

  function execute(bytes memory args) public returns (bytes memory) {
    uint256 costValue = abi.decode(args, (uint256));
    return executeTyped(costValue);
  }

  function executeTyped(uint256 costValue) public returns (bytes memory) {
    uint256 entityId = addressToEntity(msg.sender);

    CoinComponent coin = CoinComponent(getAddressById(components, CoinComponentID));
    require(coin.getValue(entityId) >= costValue, "no enough coin");

    coin.set(entityId, coin.getValue(entityId) - costValue);

    return new bytes(0);
  }
}
