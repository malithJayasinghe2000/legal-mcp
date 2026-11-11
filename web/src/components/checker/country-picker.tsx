"use client";

import { Check, ChevronsUpDown, X } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { COMMON, COUNTRIES, countryName } from "@/lib/countries";
import { cn } from "@/lib/utils";

type Props = {
  id: string;
  labelId: string;
  multiple: boolean;
  value: string[];
  onChange: (value: string[]) => void;
};

export function CountryPicker({ id, labelId, multiple, value, onChange }: Props) {
  const [open, setOpen] = useState(false);

  function toggle(code: string) {
    if (!multiple) {
      onChange([code]);
      setOpen(false);
      return;
    }
    onChange(value.includes(code) ? value.filter((c) => c !== code) : [...value, code]);
  }

  return (
    <div className="space-y-3">
      {multiple && value.length > 0 && (
        <ul className="flex flex-wrap gap-2" aria-label="Selected countries">
          {value.map((code) => (
            <li key={code}>
              <button
                type="button"
                onClick={() => toggle(code)}
                className="inline-flex items-center gap-1.5 rounded-md border border-rule bg-surface py-1 pr-2 pl-3 text-sm"
                aria-label={`Remove ${countryName(code)}`}
              >
                {countryName(code)}
                <X className="size-3.5 text-ink-muted" aria-hidden />
              </button>
            </li>
          ))}
        </ul>
      )}
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button
            id={id}
            type="button"
            variant="outline"
            role="combobox"
            aria-expanded={open}
            aria-labelledby={labelId}
            className="h-11 w-full max-w-sm justify-between bg-surface px-3 text-base font-normal"
          >
            {multiple
              ? "Add a country"
              : value[0]
                ? countryName(value[0])
                : "Choose a country"}
            <ChevronsUpDown className="size-4 text-ink-muted" aria-hidden />
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-(--radix-popover-trigger-width) p-0" align="start">
          <Command>
            <CommandInput placeholder="Search countries" />
            <CommandList>
              <CommandEmpty>No country with that name.</CommandEmpty>
              <CommandGroup>
                {COUNTRIES.map((code, i) => (
                  <CommandItem
                    key={code}
                    value={`${countryName(code)} ${code}`}
                    onSelect={() => toggle(code)}
                    className={cn(i === COMMON.length - 1 && "mb-1 border-b border-rule pb-2")}
                  >
                    <Check
                      className={cn("size-4", value.includes(code) ? "opacity-100" : "opacity-0")}
                      aria-hidden
                    />
                    {countryName(code)}
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  );
}
