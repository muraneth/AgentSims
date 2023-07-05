// FollowupSystem.ts

import {
  getComponentValue,
  defineRxSystem,
} from '@latticexyz/recs';

import { SetupResult } from '../mud/setup';
import { World } from '../world/World';
import { clientComponents } from '../mud/components';

const easingFactor = 0.1;
const targetScale = 1; // 正常比例
const scaleEasingFactor = 0.05;

const Movement = clientComponents.Movement;

export async function setup(ctx: SetupResult, world: World) {
  const viewport = world.Viewport;

  const lerp = (start: number, end: number, alpha: number) => {
    return start + alpha * (end - start);
  };

  const smoothFollow = (
    entityPosition: { x: number; y: number },
    viewportCenter: { x: number; y: number }
  ) => {
    const dx = entityPosition.x - viewportCenter.x;
    const dy = entityPosition.y - viewportCenter.y;

    const distance = Math.sqrt(dx * dx + dy * dy);
    const direction = { x: dx / distance, y: dy / distance };

    const targetPosition = {
      x: viewportCenter.x + direction.x * distance * easingFactor,
      y: viewportCenter.y + direction.y * distance * easingFactor,
    };

    return targetPosition;
  };

  let initialZoomCompleted = false;
  let lastEntityPosition = { x: 0, y: 0 };

  let enableFollow = true;

  window.addEventListener('keydown', (e) => {
    if (e.key === 'f') {
      enableFollow = true;
    }

    if (e.key === 'u') {
      enableFollow = false;
    }
  });

  defineRxSystem(ctx.world, world.$update, (_delta: number) => {
    if (enableFollow && world.SelectedEntity) {
      const entity = world.getOrCreateEntity(world.SelectedEntity);
      const movement = getComponentValue(Movement, world.SelectedEntity);

      if (entity && movement) {
        const worldX = world.EntityLayer.x + entity.x;
        const worldY = world.EntityLayer.y + entity.y;

        // 如果实体位置发生变化，设置 initialZoomCompleted 为 false
        if (lastEntityPosition.x !== worldX || lastEntityPosition.y !== worldY) {
          initialZoomCompleted = false;
          lastEntityPosition = { x: worldX, y: worldY };
        }

        // 添加缩放效果
        if (!initialZoomCompleted) {
          const newCenter = smoothFollow(
            { x: worldX, y: worldY },
            viewport.center
          );
  
          world.Viewport.moveCenter(newCenter);

          const currentScale = viewport.scale.x;
          const newScale = lerp(currentScale, targetScale, scaleEasingFactor);
          viewport.scale.set(newScale, newScale);

          // 如果缩放接近目标值，则设置 initialZoomCompleted 为 true
          if (Math.abs(newScale - targetScale) < 0.01) {
            initialZoomCompleted = true;
          }
        }
      }
    }
  });
}
