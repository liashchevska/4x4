// Hook to provide serialization and deserialization for types containing Sets.
import { useLocalStorage as useLocalStorageBase } from "usehooks-ts";

export function serialize<T>(value: T): string {
  return JSON.stringify(value, (_, v) => {
    return v instanceof Set ? { __type: "Set", values: [...v] } : v;
  });
}

function deserialize<T>(value: string, initialValue: T): T {
  try {
    if (!value) return initialValue;

    return JSON.parse(value, (k, v) => {
      if (v && v.__type === "Set") {
        return new Set(v.values);
      }
      return v;
    });
  } catch {
    return initialValue;
  }
}

export function useLocalStorage<T>(key: string, initialValue: T) {
  return useLocalStorageBase<T>(key, initialValue, {
    serializer: serialize,
    deserializer: (value) => deserialize(value, initialValue),
  });
}
