// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { addressToEntity } from "solecs/utils.sol";
import { System, IWorld } from "solecs/System.sol";
import { getAddressById } from "solecs/utils.sol";
import { AgentComponent, ID as AgentComponentID, Agent } from "components/AgentComponent.sol";
import { CoinComponent, ID as CoinComponentId } from "components/CoinComponent.sol";

uint256 constant ID = uint256(keccak256("system.Agent"));

struct AgentInput {
  string name;
  uint16 age;
  string occupation;
  string model;
  uint256 initCoin;
}

contract AgentSystem is System {
  constructor(IWorld _world, address _components) System(_world, _components) {}

  function execute(bytes memory args) public returns (bytes memory) {
    AgentInput memory inputParams = abi.decode(args, (AgentInput));
    return executeTyped(inputParams);
  }

  function executeTyped(AgentInput memory inputParams) public returns (bytes memory) {
    uint256 entityId = addressToEntity(msg.sender);

    // PlayerComponent player = PlayerComponent(getAddressById(components, PlayerComponentID));
    // require(!player.has(entityId), "already joined");

    // // Constrain position to map size, wrapping around if necessary
    // MapConfig memory mapConfig = MapConfigComponent(getAddressById(components, MapConfigComponentID)).getValue();
    // inputParams.x = (inputParams.x + int32(mapConfig.width)) % int32(mapConfig.width);
    // inputParams.y = (inputParams.y + int32(mapConfig.height)) % int32(mapConfig.height);

    // require(LibMap.obstructions(world, Coord(inputParams.x, inputParams.y)).length == 0, "this space is obstructed");
    AgentComponent agentComponent = AgentComponent(getAddressById(components, AgentComponentID));
    require(!agentComponent.has(entityId), "already joined");

    // player.set(entityId);
    Agent memory agent = Agent(inputParams.name, inputParams.age, inputParams.occupation, inputParams.model);
    agentComponent.set(entityId, agent);
    CoinComponent(getAddressById(components, CoinComponentId)).set(entityId, inputParams.initCoin);
    // PositionComponent(getAddressById(components, PositionComponentID)).set(entityId, Coord(inputParams.x, inputParams.y));
    // MovableComponent(getAddressById(components, MovableComponentID)).set(entityId);
    // EncounterableComponent(getAddressById(components, EncounterableComponentID)).set(entityId);

    return new bytes(0);
  }
}
