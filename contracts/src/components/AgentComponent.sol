// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { BareComponent } from "solecs/BareComponent.sol";
import { LibTypes } from "solecs/LibTypes.sol";

uint256 constant ID = uint256(keccak256("component.Agent"));

struct Agent {
  string name;
  uint16 age;
  string occupation;
  string model;
}

contract AgentComponent is BareComponent {
  constructor(address world) BareComponent(world, ID) {}

  function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
    keys = new string[](4);
    values = new LibTypes.SchemaValue[](4);

    keys[0] = "name";
    values[0] = LibTypes.SchemaValue.STRING;

    keys[1] = "age";
    values[1] = LibTypes.SchemaValue.UINT16;

    keys[2] = "occupation";
    values[2] = LibTypes.SchemaValue.STRING;

    keys[3] = "model";
    values[3] = LibTypes.SchemaValue.STRING;
  }

  function set(uint256 entity, Agent memory agent) public {
    set(entity, abi.encode(agent.name, agent.age, agent.occupation, agent.model));
  }

  function getValue(uint256 entity) public view returns (Agent memory) {
    (string memory name, uint16 age, string memory occupation, string memory model) = abi.decode(getRawValue(entity), (string, uint16, string, string));
    return Agent(name, age, occupation, model);
  }
}
