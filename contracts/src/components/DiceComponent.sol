// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;
import { BareComponent } from "solecs/BareComponent.sol";
import { LibTypes } from "solecs/LibTypes.sol";
import { SingletonID } from "solecs/SingletonID.sol";

uint256 constant ID = uint256(keccak256("component.Dice"));

enum Dice {
    Ace,
    Deuce,
    Trey,
    Four,
    Five,
    Six
}

// enum RANK {
//     Ace,
//     Two,
//     Three,
//     Four,
//     Five,
//     Six,
//     Seven,
//     Eight,
//     Nine,
//     Ten,
//     Jack,
//     Queen,
//     King
// }

// struct Card {
//   SUIT suit;
//   RANK rank;
// }

// struct Cards {
//     Card[] cards;
// }
struct DiceResult {
  Dice dice1;
}

contract DiceComponent is BareComponent {
  constructor(address world) BareComponent(world, ID) {}

  function getSchema() public pure override returns (string[] memory keys, LibTypes.SchemaValue[] memory values) {
    keys = new string[](1);
    values = new LibTypes.SchemaValue[](1);

    keys[0] = "dice1";
    values[0] = LibTypes.SchemaValue.UINT32;
  }

  function set(uint256 entity, DiceResult calldata value) public virtual {
    set(entity, abi.encode(value));
  }

  function getValue(uint256 entity) public view virtual returns (DiceResult memory) {
    (Dice dice1) = abi.decode(getRawValue(entity), (Dice));
    return DiceResult(dice1);
  }
}
