import { defineQuery, QueryFragment } from "@latticexyz/recs";
import { useEffect, useMemo, useState } from "react";
import { useDeepMemo } from "../utils/useDeepMemo";
import { map } from "rxjs";

// This does a little more rendering than is necessary when arguments change,
// but at least it's giving correct results now. Will optimize later!

export function useEntityQueryExt(fragments: QueryFragment[]) {
  const stableFragments = useDeepMemo(fragments);
  const query = useMemo(() => defineQuery(stableFragments, { runOnInit: true }), [stableFragments]);
  const [entities, setEntities] = useState([...query.matching]);

  useEffect(() => {
    setEntities([...query.matching]);
    const subscription = query.update$
      .pipe(map(() => [...query.matching]))
      .subscribe((entities) => setEntities(entities));
    return () => subscription.unsubscribe();
  }, [query]);

  return entities;
}