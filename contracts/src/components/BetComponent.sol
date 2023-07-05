// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { BareComponent } from "solecs/BareComponent.sol";
import { LibTypes } from "solecs/LibTypes.sol";
import { SingletonID } from "solecs/SingletonID.sol";

uint256 constant ID = uint256(keccak256("component.Bet"));

enum Bet {
    Little,
    Big
}

struct BetResult {
  Bet bet;
}

contract DiceComponent is BareComponent {
  constructor(address world) BareComponent(world, ID) {}

  function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
    keys = new string[](1);
    values = new LibTypes.SchemaValue[](1);

    keys[0] = "bet";
    values[0] = LibTypes.SchemaValue.UINT32;
  }

  function set(uint256 entity, BetResult calldata value) public virtual {
    set(entity, abi.encode(value));
  }

  function getValue(uint256 entity) public view virtual returns (BetResult memory) {
    (Bet bet) = abi.decode(getRawValue(entity), (Bet));
    return BetResult(bet);
  }
}
