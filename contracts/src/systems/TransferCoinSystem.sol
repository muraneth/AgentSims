// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { System, IWorld } from "solecs/System.sol";
import { getAddressById, addressToEntity } from "solecs/utils.sol";
import { CoinComponent, ID as CoinComponentID } from "components/CoinComponent.sol";

uint256 constant ID = uint256(keccak256("system.TransferCoin"));

struct InputParams {
    uint256 targetId;
    uint256 transferValue;
}

contract TransferCoinSystem is System {
  constructor(IWorld _world, address _components) System(_world, _components) {}

  function execute(bytes memory args) public returns (bytes memory) {
    InputParams memory inputParams = abi.decode(args, (InputParams));
    return executeTyped(inputParams);
  }

  function executeTyped(InputParams memory inputParams) public returns (bytes memory) {
    uint256 entityId = addressToEntity(msg.sender);

    CoinComponent coin = CoinComponent(getAddressById(components, CoinComponentID));
    require(coin.getValue(entityId) >= inputParams.transferValue, "no enough coin");
    require(coin.getValue(inputParams.targetId) + inputParams.transferValue >= coin.getValue(inputParams.targetId), "math error");

    coin.set(entityId, coin.getValue(entityId) - inputParams.transferValue);
    coin.set(inputParams.targetId, coin.getValue(inputParams.targetId) + inputParams.transferValue);

    return new bytes(0);
  }
}
