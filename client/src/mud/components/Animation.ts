import { defineComponent, Metadata, Type, World } from "@latticexyz/recs";

const Animation = {
  animation: Type.OptionalString,
} as const;

export function defineAnimationComponent<M extends Metadata>(
  world: World,
  options?: { id?: string; metadata?: M; indexed?: boolean }
) {
  return defineComponent<typeof Animation, M>(world, {
    animation: Type.OptionalString,
  }, options);
}